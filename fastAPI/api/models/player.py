from typing import List

#from app.models.common import DateTimeModelMixin, IDModelMixin
#from app.models.domain.profiles import Profile
#from app.models.domain.rwmodel import RWModel
from api.models.common import CvModel, CvSchema




# simple biography
class mdlPlayer(CvModel):
	uid:str
	chip:int
	name:str
	card: List[int]




# ------------------------ schemas ---------------------------


## ---------- bio ---------------

class scmPlayerCreate(CvSchema):
	name :str
	birthday :str
	address :str | None = None
	iconpath :str | None = None
	educations  :str | None = None
	languages :str | None = None 
	certifications :str | None = None



class scmPlayerUpdate(CvSchema):
	name :str | None = None
	birthday :str | None = None
	address :str | None = None
	iconpath :str | None = None
	educations  :str | None = None
	languages :str | None = None 
	certifications :str | None = None

	"""
	@classmethod
	def to_dict(cls):
		# Noneでないクラス変数のみ辞書に追加
		return {k: v for k, v in cls.__dict__.items() if not k.startswith('__') and v is not None}

	@classmethod
	def to_dict_e(cls):
		# クラス変数の中から、Noneでないものを選んで辞書に追加
		result = {}
		for key, value in cls.__dict__.items():
			if not key.startswith('__') and value is not None:
				result[key] = value
		return result
	"""


## ---------- bio sub ---------------

class scmPlayerEducation(CvModel):
	name : str
	description : str


class scmListPlayerEducation(CvModel):
    objs: List[scmPlayerEducation]
    count: int


class scmPlayerLanguage(CvModel):
	name : str
	description : str


class scmListPlayerLanguage(CvModel):
    objs: List[scmPlayerLanguage]
    count: int






