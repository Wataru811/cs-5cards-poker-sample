from typing import List

#from app.models.common import DateTimeModelMixin, IDModelMixin
#from app.models.domain.profiles import Profile
#from app.models.domain.rwmodel import RWModel
from api.models.common import CvModel, CvSchema





# simple biography
class mdlGame(CvModel):
	uuid :str
	deck : List[int] 

class mdlPoker(CvModel):
	uuid :str
	deck : List[int] 





# ------------------------ schemas ---------------------------


## ---------- bio ---------------

class scmPokerCreate(CvSchema):
	name :str
	birthday :str
	address :str | None = None
	iconpath :str | None = None
	educations  :str | None = None
	languages :str | None = None 
	certifications :str | None = None



class scmPokerUpdate(CvSchema):
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

class scmPokerEducation(CvModel):
	name : str
	description : str


class scmListPokerEducation(CvModel):
    objs: List[scmPokerEducation]
    count: int


class scmPokerLanguage(CvModel):
	name : str
	description : str


class scmListPokerLanguage(CvModel):
    objs: List[scmPokerLanguage]
    count: int






