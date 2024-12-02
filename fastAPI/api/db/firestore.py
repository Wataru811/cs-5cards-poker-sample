#import os
import copy
from firebase_admin import firestore
from datetime import datetime,timezone
from dateutil import tz


#  required (env) GOOGLE_APPLICATION_CREDENTIALS
fbDB = firestore.client()
CO_USER = "user"
CO_PROFILE = "userProf"
#CO_BIO = "bio"
CO_LANG= "Lang"
#CO_BIO_EDU= "bioEdu"
CO_POKER = "poker"

#env_var = os.environ
#TIME_FORMAT='%Y-%m-%d %H:%M:%S'


# firebase  ----------------------------

kldBase = { 
			"id":"",  
			"uid":"",  
			"group":"",  
			"created":"",
			"image":"",
			"body":"",
		  }


# firebase  ----------------------------
def getCo( co_name ):
	return fbDB.collection(co_name)

# READ
def getFs( co_name, id ):
	co = getCo(co_name)
	if co:
		ref = co.document( id )
		doc = ref.get()
		if not doc.exists:
			return None
		dd = doc.to_dict()		
		return dd	
	return( None )


# CREATE 
def addFs( co_name, id, data ):
	co = getCo(co_name)
	if co:
		del data["id"]
		updatetiem, ref = co.add( data )
		return( ref.id )
	return( None )


# UPDATE 
def updateFs( co_name, id, data ):
	co = getCo(co_name)
	if co:
		try:
			ref = co.document( id )
			ref.update( {"body": data })
			return data
		except:
			return None
	return None

# DELETE
def deleteFs( co_name, id ):
	co = getCo(co_name)
	if co:
		ref = co.document( id )
		doc = ref.get()
		if doc.exists:
			co.document( id ).delete()
			return id
	return None



# ------- user --------

def getUserDB():
	return fbDB.collection(CO_USER)

def getUserProfileDB():
	return fbDB.collection(CO_PROFILE)

# user CRUD 
def getUserById(id):
	return getFs( CO_USER, id )

def addUserById(id,data):
	return addFs( CO_USER, id,data )

def updateUserById(id,data):
	return updateFs( CO_USER, id,data )

def deleteUserById(id):
	return deleteFs( CO_USER, id)

# userProfile CRUD 
def getProfileById(id):
	return getFs( CO_PROFILE, id )

def addProfileById(id,data):
	return addFs( CO_PROFILE, id,data )

def updateProfileById(id,data):
	return updateFs( CO_PROFILE, id,data )

def deleteUserById(id):
	return deleteFs( CO_PROFILE, id)


# bio CRUD 




