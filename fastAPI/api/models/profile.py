from typing import List

#from app.models.common import DateTimeModelMixin, IDModelMixin
#from app.models.domain.profiles import Profile
#from app.models.domain.rwmodel import RWModel
from api.models.common import CvModel, CvSchema


#
class mdlProfile(CvModel):
	name :str
	birthday :str
	address :str
	iconpath :str
	educations  :str
	languages :str
	certifications :str

class mdlProfileEducation(CvModel):
	#owner: str
	name : str
	description : str

class mdlProfileLanguage (CvModel):
	#owner : str
	Name :str 
	Level :str


# ------------------------ schemas ---------------------------


## ---------- bio ---------------

class scmProfileCreate(CvSchema):
	name :str
	birthday :str
	address :str | None = None
	iconpath :str | None = None
	educations  :str | None = None
	languages :str | None = None 
	certifications :str | None = None



class scmProfileUpdate(CvSchema):
	name :str | None = None
	birthday :str | None = None
	address :str | None = None
	iconpath :str | None = None
	educations  :str | None = None
	languages :str | None = None 
	certifications :str | None = None


## ---------- bio sub ---------------

class scmProfileLanguage(CvModel):
	name : str
	description : str


class scmListProfileLanguage(CvModel):
    objs: List[scmProfileLanguage]
    count: int






