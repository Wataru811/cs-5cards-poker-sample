"""

--- kokono share ---




"""

from fastapi import Depends, APIRouter  #UploadFile, Body, File, Form, Request 
from fastapi import HTTPException 	#, status, Response, BackgroundTasks
from pydantic import BaseModel
from firebase_admin import firestore
from typing import List,Annotated
import os,sys
sys.path.append("..")
#import uuid
#import boto3

from config.firebaseConfig import get_firebase_user_from_token,get_current_user
#from .cloudUtil import ,  getKldDB,getShareDB,getUserDB, fetchKld, getS3,getKld ,storeKld ,BUCKET_NAME


"""
env_var = os.environ
AWS_KEY=env_var["KOKONO_AWS_KEY"]
AWS_SECRET=env_var["KOKONO_AWS_SECRET"]
REGION_NAME= env_var['KOKONO_AWS_REGION'] 
BUCKET_NAME = env_var['KOKONO_AWS_S3_BUCKET'] 
"""

# ------------------- config ---------------------

# ------------------- router ---------------------
router = APIRouter(
	prefix="/userprof",
	tags=["userprof"],
	responses={404: {"description": "Not found"}},
)

# ----------- multi object selector --------------
#class mdlIdList(BaseModel):
# 	ids: list[str] = []


@router.get("/{id}")
def get( id:str, user: Annotated[dict, Depends(get_current_user)]):
	# バリデーション入れる
	db = getUserDB()
	query = db.where('uid', '==',id)
	#items = []
	for item in query.stream():
		data = item.to_dict()
		#data["id"] =  share.id
		#docId=data["docId"]
		#doc = fetchKld(docId)
		#doc["id"] = docId
		return {"status":"ok", "data":data}
	return {"status":"error", "reason":"Not found"}

	"""
	doc_ref = db.document( id )
	doc = doc_ref.get()
	
	if doc.exists:
		return { "status":"ok", "data":doc.to_dict() }
	else:
		return { "status":"error", "reason":"Item not found" }
	"""
		#//raise HTTPException(status_code=404, detail="Item not found")
		#return None

class mdlUserProf(BaseModel):
	# oauth	
	uid:str
	name:str
	email:str
	provider: str
	# app 
	lang: str = "en" 
	nickname:str | None


#class mdlUserProfGet(mdlUserProfUpdate):
#	id: str 

@router.post("/")
async def addUser( mdl: mdlUserProf, user: Annotated[dict, Depends(get_current_user)]):
	db = getUserDB()
	updatetiem, ref = db.add( mdl.dict())
	return( {"status":"ok","id":ref.id} )
	


@router.put("/{id}")
async def updateUser( mdl: mdlUserProf, user: Annotated[dict, Depends(get_current_user)]):
	print( mdl.dict())
	uid = mdl.dict()["uid"]
	db = getUserDB()
	query = db.where('uid', '==',uid)
	print(query)
	#items = []
	for item in query.stream():
		print(item)
		print(item.id)
		ref = db.document( item.id )
		ref.update( mdl.dict()  ) 
		return {"status":"ok"}
	raise HTTPException(status_code=404, detail="Item not found")
	
	"""
	try:
		ref = db.document( id )
		ref.update( mdl.dict()  ) 
	except:
		raise HTTPException(status_code=404, detail="Item not found")
	return {"status":"ok"}
	"""





