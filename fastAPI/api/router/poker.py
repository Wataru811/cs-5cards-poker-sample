from datetime import datetime
from dateutil import tz
from fastapi import Depends, APIRouter  #UploadFile, Body, File, Form, Request 
from fastapi import HTTPException 	#, status, Response, BackgroundTasks
#from pydantic import BaseModel
from firebase_admin import firestore
from typing import List,Annotated
#from app.models.common import mdlIdList
import os,sys
sys.path.append("..")

from config.firebaseConfig import get_firebase_user_from_token,get_current_user
#from .cloudUtil import getS3Url,  getKldDB,getShareDB,getUserDB, fetchKld, getS3,getKld ,storeKld ,BUCKET_NAME
#from util.mailUtil  import shareKokono
#from .apiAuth import getUserInfoByUID

from api.db.firestore import CO_USER, CO_PROFILE,CO_POKER,CO_LANG
from api.db.firestore import getFs,addFs,deleteFs,updateFs
import api.models.poker as pokerModels
from api.models.common import classToDictByNNV

"""
env_var = os.environ
AWS_KEY=env_var["POKER_AWS_KEY"]
AWS_SECRET=env_var["POKER_AWS_SECRET"]
REGION_NAME= env_var['POKER_AWS_REGION'] 
BUCKET_NAME = env_var['POKER_AWS_S3_BUCKET'] 
"""

# ------------------- config ---------------------

# ------------------- router ---------------------
router = APIRouter(
	prefix="/poker",
	tags=["poker"],
	responses={404: {"description": "Not found"}},
)


@router.get("/{id}")
def get( id:str, user: Annotated[dict, Depends(get_current_user)]):
	# バリデーション入れる
	print(user)
	doc = getFs(CO_poker,id, owner=user["id"])
	if doc==None:
		raise HTTPException(status_code=404, detail="[x001] Item not found")
	return {"status":"ok", "item":doc}


# list of
@router.get("/")
async def pokerByUser( user: Annotated[dict, Depends(get_current_user)]):
	# バリデーション入れる
	print(user)
	items = getFsListById(CO_poker,user["id"])
	if items==None:
		raise HTTPException(status_code=404, detail="[x001] Item not found")
	return {"status":"ok", "items":items}


@router.post("/")
def create( obj:pokerModels.mdlPoker, user: Annotated[dict, Depends(get_current_user)]):
	# バリデーション入れる
	doc = addFs(CO_poker,obj, owner=user["id"])
	if doc==None:
		raise HTTPException(status_code=404, detail="create error")
	return doc


@router.put("/{id}")
async def updateBody( obj:pokerModels.scmPokerUpdate, user: Annotated[dict, Depends(get_current_user)]):
	dictUpdate = classToDictByNNV(obj)
	doc = updateFs(CO_poker,id,dictUpdate , owner=user["id"])
	if doc==None:
		raise HTTPException(status_code=404, detail="content not found")
	return {"status":"ok", "item":doc }
	