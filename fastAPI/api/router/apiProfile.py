from datetime import datetime
from dateutil import tz
from fastapi import Depends, APIRouter  #UploadFile, Body, File, Form, Request 
from fastapi import HTTPException 	#, status, Response, BackgroundTasks
from pydantic import BaseModel
from firebase_admin import firestore
from typing import List,Annotated
#from app.models.common import mdlIdList
import os,sys
sys.path.append("..")

from config.firebaseConfig import get_firebase_user_from_token,get_current_user
#from .cloudUtil import getS3Url,  getKldDB,getShareDB,getUserDB, fetchKld, getS3,getKld ,storeKld ,BUCKET_NAME
#from util.mailUtil  import shareKokono
#from .apiAuth import getUserInfoByUID

from api.db.firestore import CO_USER, CO_PROFILE,CO_profile,CO_profile_LANG, CO_profile_EDU
from api.db.firestore import getFs,addFs,deleteFs,updateFs
import api.models.profile as profileModels
from api.models.common import classToDictByNNV

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
	prefix="/profile",
	tags=["profile"],
	responses={404: {"description": "Not found"}},
)

"""
def convertQuery2Ary( query):
	items = []
	for doc in query.stream():
		items.append(dict( **{ "id":doc.id}, **doc.to_dict() )  )
	return items	


# ----------- multi object selector --------------
class mdlIdList(BaseModel):
	ids: list[str] = []
"""


@router.get("/{id}")
def get( id:str, user: Annotated[dict, Depends(get_current_user)]):
	# バリデーション入れる
	print(user)
	doc = getFs(CO_profile,id, owner=user["id"])
	if doc==None:
		raise HTTPException(status_code=404, detail="[x001] Item not found")
	return {"status":"ok", "item":doc}


# list of
@router.get("/")
async def profileByUser( user: Annotated[dict, Depends(get_current_user)]):
	# バリデーション入れる
	print(user)
	items = getFsListById(CO_profile,user["id"])
	if items==None:
		raise HTTPException(status_code=404, detail="[x001] Item not found")
	return {"status":"ok", "items":items}


	"""
	query = db.where('uid', '==', user["id"])
	#items = convertQuery2Ary( query )
	items = []
	for doc in query.stream():
		kld=dict( **{ "id":doc.id}, **doc.to_dict() )  
		items.append( {"kld":kld, "sharing":{}, "shared":{} } )	
	"""
	return {"status":"ok", "items":items}


@router.post("/")
def create( obj:profileModels.mdlprofile, user: Annotated[dict, Depends(get_current_user)]):
	# バリデーション入れる
	doc = addFs(CO_profile,obj, owner=user["id"])
	if doc==None:
		raise HTTPException(status_code=404, detail="create error")
	return doc

@router.put("/{id}")
async def updateBody( obj:profileModels.scmprofileUpdate, user: Annotated[dict, Depends(get_current_user)]):
	dictUpdate = classToDictByNNV(obj)
	doc = updateFs(CO_profile,id,dictUpdate , owner=user["id"])
	if doc==None:
		raise HTTPException(status_code=404, detail="content not found")
	return {"status":"ok", "item":doc }
	
	"""
	try:
		ref = db.document( mdl.id )
		ref.update( {"body": mdl.body })
	except:
		raise HTTPException(status_code=404, detail="Item not found")
	return {"status":"ok"}
	"""

@router.delete("/{id}")
async def deleteprofile( id: str, user: Annotated[dict, Depends(get_current_user)]):
	doc = deleteFs(CO_profile,id, owner=user["id"])
	"""
	doc_ref = getShareDB().document( id )
	doc = doc_ref.get()
	"""
	if doc==None:
		raise HTTPException(status_code=404, detail="content not found")
	return  {"status":"ok", "id":id}




"""
class mdlBody(BaseModel):
	id: str 
	body: str 

@router.put("/")
async def kokonoUpdateBody( mdl: mdlBody, user: Annotated[dict, Depends(get_current_user)]):
	db = getKldDB()
	try:
		ref = db.document( mdl.id )
		ref.update( {"body": mdl.body })
	except:
		raise HTTPException(status_code=404, detail="Item not found")
	return {"status":"ok"}

# ------------------- share -----------------------
class mdlShare(BaseModel):
	pub: bool=False,  #public
	docId: str
	created: str | None = None
	idFrom : str
	mailTo: str  | None = None
	mailResult : bool = None 
	dtLimit : str  | None = None

@router.delete("/share/{id}")
async def deleteShare( id: str, user: Annotated[dict, Depends(get_current_user)]):
	doc_ref = getShareDB().document( id )
	doc = doc_ref.get()
	if doc.exists:
		getShareDB().document( id ).delete()
		return  {"status":"ok"}
	else:
		raise HTTPException(status_code=404, detail="content not found")

def getShareUrl(id, isPublic) :
	BASE_URL = os.environ["FRONTEND_URL"]  ## localhost or staging/product web address
	if isPublic:
		return BASE_URL + "/pub/share?id=" + id
	else:	
		return BASE_URL + "/kf/share?id=" + id

@router.post("/share")
async def createShare( mdl: mdlShare, user: Annotated[dict, Depends(get_current_user)]):
	db = getShareDB() 
	# check same data
	db= db.where(filter=firestore.FieldFilter("docId", "==", mdl.docId))
	db= db.where(filter=firestore.FieldFilter("idFrom", "==", mdl.idFrom))
	db= db.where(filter=firestore.FieldFilter("mailTo", "==", mdl.mailTo))
	docs = db.get()
	if len(docs) > 0:
		items = []
		for doc in docs:
			items.append(dict( **{ "id":doc.id}, **doc.to_dict() )  )
			db = getShareDB() 
			ref = db.document(doc.id)
			ref.update({"pub": mdl.pub})
			if mdl.mailTo != "":
				url = getShareUrl(doc.id ,mdl.pub )
				shareKokono( mdl.mailTo, user["name"],user["email"] ,url , "" )		
			return {"status":"exist", "item":items[0]}

	# add data
	db = getShareDB()
	jst = tz.gettz("Asia/Tokyo")
	mdl.created = datetime.now(jst).isoformat()
	item, ref = db.add( mdl.dict())
	if mdl.mailTo != "":
		url = getShareUrl(ref.id ,mdl.pub )
		shareKokono( mdl.mailTo, user["name"],user["email"] ,url , "" )		
	newItem = mdl.dict()	
	newItem["id"] = ref.id


	return( {"status":"ok","item":newItem} )
"""


def getShareDoc (id, sharedUserMail=None):
	db =getShareDB() 
	doc_ref = db.document( id )
	doc = doc_ref.get()
	if not doc.exists:
		return None
	dd = doc.to_dict()		
	if not doc.exists:
		raise HTTPException(status_code=404, detail="[x007] content does not exits")
	#if sharedUserMail:
	#	if dd["mailTo"] != "" and dd["mailTo"] != sharedUserMail:
	#		raise HTTPException(status_code=404, detail="[x005] Item not found")

	# get document 	
	doc = fetchKld(dd["docId"])
	if doc == None:
		raise HTTPException(status_code=404, detail="[x000] Item not found")
	"""
	# get owner	
	db =getUserDB()
	docs= db.where(filter=firestore.FieldFilter("uid", "==", doc["owner"])).stream()
	for owner in docs:
		return  { "kld":doc, "owner":owner.to_dict()}
	"""
	userInfo = getUserInfoByUID( doc["uid"] )	
	return  { "kld":doc, "owner":userInfo}
	#return 	None
"""
@router.get("/share/{id}")
async def getShare( id:str, user: Annotated[dict, Depends(get_current_user)]):
	ret = getShareDoc(id, user["email"])
	if ret == None:
		raise HTTPException(status_code=404, detail="[x001] Item not found")
	return ret

@router.get("/public-share/{id}")
async def getShare( id:str):
	ret = getShareDoc(id)
	if ret == None:
		raise HTTPException(status_code=404, detail="[x002] Item not found")
	return ret


"""