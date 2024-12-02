from datetime import timedelta, datetime
from typing import Annotated
from fastapi import Form, Depends, HTTPException, APIRouter, Response,status
from firebase_admin import auth, credentials,exceptions,firestore
import datetime

import sys
sys.path.append("..")
from config.firebaseConfig import get_firebase_user_from_token,get_current_user
from pydantic import BaseModel
from .cloudUtil import getUserDB , fbDB 


router = APIRouter()

@router.get("/ping")
async def api_ping():
    return {"status": "ok"}


@router.get("/auth-test")
async def get_userId(user: Annotated[dict, Depends(get_firebase_user_from_token)]):
    """gets the firebase connected user"""
    return {"id": user["uid"]}


@router.get("/session-test")
async def getUidBySessionToken(user: Annotated[dict, Depends(get_current_user)]):
    return {"status":"ok", "user":user}

# ----------------  login ----------------

class mdlToken(BaseModel):
    idToken: str
    lang:str

@router.post("/login")
async def get_sessionToken( mdl:mdlToken, response: Response ):
    """ IdToken to sessionToken by firebase 
        input: id-token
        output: session-token 
    """

    try:
        decoded_token = auth.verify_id_token(mdl.idToken)
        uid = decoded_token['uid']
        (exist, userInfo) =  isUser(decoded_token["uid"])
        if not exist:
            createUserInfo(decoded_token,mdl.lang)  
        expires_in = timedelta(days=5)  # Cookieの有効期限
        session_cookie = auth.create_session_cookie(mdl.idToken, expires_in=expires_in)
        """
        decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
        expires = datetime.datetime.now(datetime.timezone.utc) + expires_in
        response.set_cookie(
            key='session',
            value=session_cookie, 
            expires=expires, 
            httponly=True, 
            secure=True
        )
        """
        return { 'status':'ok', "token":session_cookie  ,"user":userInfo }
    except exceptions.FirebaseError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
            #headers={"WWW-Authenticate": "Basic"},
        )


def isUser(uid: str) -> bool:
    db = fbDB.collection("userProf")
    query = db.where(filter=firestore.FieldFilter("uid", "==", uid))
    items = []
    for doc in query.stream():
        item=dict( **{ "id":doc.id}, **doc.to_dict() )  
        items.append( item )    
    if len(items) > 0:
        return (True, items[0])
    return (False, None)


# ---------------- user info ----------------
KEY_IMG_CNT = "imgCnt"
class mdlUserInfo(BaseModel):
    uid: str
    name: str
    nickname: str
    email: str    
    provider: str
    lang : str
    imgCnt: int = 0

def createUserInfo( user, lang ):
    info = {} 
    langs = [ "ja","en","vi"] 
    if not lang in langs:
        lang = "en"
    info[KEY_IMG_CNT] =0 
    info["lang"] = lang 
    info["uid"]      = user["uid"]
    info["email"]    = user["email"]
    if "name" in user:
        info["name"]     = user['name']
        info["nickname"] = user["name"]
    else:
        info["name"]     = user['email']
        info["nickname"] = user["email"]
 
    info["provider"] = user["firebase"]["sign_in_provider"]
    info["status"] = "new" 
    db = getUserDB()
    ref = db.add(info)

# get user info
def getUserInfoByUID( uid ):
    db = getUserDB()
    docs= db.where(filter=firestore.FieldFilter("uid", "==", uid)).stream()
    for owner in docs:
        return  owner.to_dict()
    return None

#  update user info
def updateUserInfoByUID( uid,dict):
    db = getUserDB()
    docs= db.where(filter=firestore.FieldFilter("uid", "==", uid)).stream()
    for owner in docs:
        db.document(owner.id).update(dict)
        return owner.to_dict()
    return None


IMG_CNT_MAX = 1000
def userInfoImageCount( uid, val ) :
    user = getUserInfoByUID(uid)
    cnt = 0
    if  KEY_IMG_CNT in user.keys():
        cnt = user[KEY_IMG_CNT] 
    cnt = cnt + val
    if cnt < 0:
        cnt = 0
    updateUserInfoByUID(uid, { KEY_IMG_CNT: cnt})


