import firebase_admin
import os
import uuid
#import boto3
import copy
from firebase_admin import firestore
from datetime import datetime,timezone
import time
from dateutil import tz

#fbApp = firebase_admin.initialize_app()
fbDB = firestore.client()

env_var = os.environ
AWS_KEY=env_var["KOKONO_AWS_KEY"]
AWS_SECRET=env_var["KOKONO_AWS_SECRET"]
REGION_NAME= env_var['KOKONO_AWS_REGION'] 
BUCKET_NAME = env_var['KOKONO_AWS_S3_BUCKET'] 

TIME_FORMAT='%Y-%m-%d %H:%M:%S'


# firebase  ----------------------------


# kld ----------------------------
kldBase = { 
			"id":"",  
			"uid":"",  
			"group":"",  
			"created":"",
			"image":"",
			"body":"",
		  }


# firebase  ----------------------------
def getKldDB():
	return fbDB.collection("kld")

def getUserDB():
	return fbDB.collection("userProf")

def getShareDB():
	return fbDB.collection("share")

def isUser(uid: str) -> bool:
	db = fbDB.collection("userProf")
	#print(db)
	docs= db.where(filter=firestore.FieldFilter("uid", "==", uid))
	docs = db.get()
	#print(docs)
	if len(docs) > 0:
		return (True, docs[0].to_dict())
	return (False, None)



"""
# AWS ----------------------------
def getS3():
	return boto3.client("s3", 
			region_name= REGION_NAME,
			aws_access_key_id=AWS_KEY,
			aws_secret_access_key=AWS_SECRET ,          
		)

def getS3Url(s3path):
	return "https://%s.s3-%s.amazonaws.com/%s" % (BUCKET_NAME, REGION_NAME, s3path)


"""
