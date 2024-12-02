"""
googletrans のために、　fastAPI 0.101.1 に固定。
-> googletrans は httpx 0.13.3 が必要なため。
"""
import json
import copy
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from langdetect import detect
from googletrans import Translator
from fastapi import Form, Depends, HTTPException, APIRouter, Response,status
from google.cloud.firestore_v1.base_query import FieldFilter
from config.firebaseConfig import get_firebase_user_from_token,get_current_user
from pydantic import ConfigDict, Field, BaseModel
from .cloudUtil import fbDB 


COLLECTION_i18n = "i18n" 

# i8n --------------------------
class mdlLocale(BaseModel):
    text: str

tr = Translator()
db = fbDB


TEXT_LEN = 200
# ------------------- router ---------------------
router = APIRouter(
    prefix="/sys/i18n",
    tags=["i18n"],
    responses={404: {"description": "Not found"}},
)
FN_i18n = "./i18n/i18n.json"

# ------------------- api ---------------------
@router.post("/"   )
async def create_i18n(
    mdl: mdlLocale
   # ,user: Annotated[dict, Depends(get_firebase_user_from_token)]
):
    if len(mdl.text) > TEXT_LEN:
        print("too long text, abort.")
        return {"status": "error", "msg": "too long text. "}
    # print(mdl.text)
    add_i18n(mdl.text)
    return {"status": "ok"}


@router.get("/")
def get_i18n(
    # bgTasks: BackgroundTasks,
    # //current_user: User = Depends(get_current_active_user),
):
    # print(FN_i18n)
    with open(FN_i18n, "r") as json_file:
        data = json.load(json_file)

    return {"status": "ok", COLLECTION_i18n: data}


# -------------------------------------------------
# firestore


"""
# 新しいドキュメントを追加する関数
def add_data(collection_name, document_data):
    doc_ref = db.collection(collection_name).document()
    doc_ref.set(document_data)
"""


# ユニーク検証用
def dataExists(collection_name, field, value):
    docs = (
        db.collection(collection_name)
        .where(filter=FieldFilter(field, "==", value))
        .stream()
    )
    for doc in docs:
        return True
    return False


# ドキュメントを検索する関数
def search_data(collection_name, field, value):
    docs = (
        db.collection(collection_name)
        .where(filter=FieldFilter(field, "==", value))
        .stream()
    )
    ret = []
    for doc in docs:
        dd = doc.to_dict()
        dd["id"] = doc.id
        ss = json.dumps(dd)
        ret.append(json.loads(ss))
    return ret


# ドキュメントを削除する関数
#def delete_data(collection_name, document_id):
#    db.collection(collection_name).document(document_id).delete()


# -------------------------------------------------
# translation & export

# tr = SyncTranslator()
def getLang(text):
    lang1 = detect(text)
    if lang1 != "ja" and lang1 != "vi":
        lang1 = "en"
    return lang1


def Translate(text, langsOrg):
    langs = copy.deepcopy(langsOrg)
    lang1 = getLang(text)
    if not lang1 in langs:
        return None
    langs = [s for s in langs if s != lang1]
    res = {lang1: text}
    for ll in langs:
        trs = tr.translate(text, src=lang1, dest=ll)  # .text
        res[ll] = trs.text
    return res


def add_i18n(text):
    lang = getLang(text)
    if dataExists(COLLECTION_i18n, lang, text):
        # print("exits!")
        return None
    langList = ["ja", "en", "vi"]
    res = Translate(text, langList)
    if res == None:
        return
    #add_data(COLLECTION_i18n, res)
    doc_ref = db.collection(COLLECTION_i18n).document()
    doc_ref.set(res)
    exportJson("./i18n/i18n.json")
    return res


def getJson():
    docs = db.collection(COLLECTION_i18n).stream()
    lst = []
    for doc in docs:
        lst.append(doc.to_dict())
    return lst


def exportJson(filename):
    # print("output > " + filename)
    data = getJson()
    print(data)
    with open(filename, "w") as json_file:
        json.dump(data, json_file)
