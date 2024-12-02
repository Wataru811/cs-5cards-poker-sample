import os
import boto3
#from firebase_admin import firestore
#from datetime import datetime,timezone
#from dateutil import tz

env_var = os.environ
AWS_KEY=env_var["_AWS_KEY"]
AWS_SECRET=env_var["_AWS_SECRET"]
REGION_NAME= env_var['_AWS_REGION'] 
BUCKET_NAME = env_var['_AWS_S3_BUCKET'] 

TIME_FORMAT='%Y-%m-%d %H:%M:%S'


# AWS ----------------------------
def getS3():
	return boto3.client("s3", 
			region_name= REGION_NAME,
			aws_access_key_id=AWS_KEY,
			aws_secret_access_key=AWS_SECRET ,          
		)

def getS3Url(s3path):
	return "https://%s.s3-%s.amazonaws.com/%s" % (BUCKET_NAME, REGION_NAME, s3path)

