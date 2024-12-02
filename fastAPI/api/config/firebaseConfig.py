import os
import pathlib
from functools import lru_cache
from typing import Annotated, Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
#from pydantic_settings import BaseSettings
from firebase_admin import credentials, initialize_app,firestore
from firebase_admin import auth  #, credentials,exceptions

# 環境変数にGOOGLE_APPLICATION_CREDENTIALS="fullpath/service-account-file.json" 設定が必要
default_app = initialize_app()    
basedir = pathlib.Path(__file__).parents[1]
bearer_scheme = HTTPBearer(auto_error=False)



# ==================  使ってない =======================
"""
FastAPI/pydantic の設定
"""

"""Main settings"""
"""
class Settings(BaseSettings):
    app_name: str = "kokono"
    env: str = os.getenv("ENV", "development")   # env は gunicorn でも制御します

    # Needed for CORS
    frontend_url: str = os.getenv("FRONTEND_URL", "NA")
"""


"""Retrieves the fastapi settings"""
"""
@lru_cache
def get_settings() -> Settings:
    return Settings()
"""

# =========================================


"""
auth depends で使用

Depends(get_firebase_user_from_token)


"""
def get_firebase_user_from_token(
    token: Annotated[Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)],
) -> Optional[dict]:
    """Uses bearer token to identify firebase user id
    Args:
        token : the bearer token. Can be None as we set auto_error to False
    Returns:
        dict: the firebase user on success
    Raises:
        HTTPException 401 if user does not exist or token is invalid
    """
    try:
        if not token:
            # raise and catch to return 401, only needed because fastapi returns 403
            # by default instead of 401 so we set auto_error to False
            raise ValueError("No token")
        user = auth.verify_id_token(token.credentials)
        return user

    # lots of possible exceptions, see firebase_admin.auth,
    # but most of the time it is a credentials issue
    except Exception:
        # see https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in or Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

"""
401 InvalidSessionCookieError 
40Invalid authentication credentials 
"""
def check_sessionToken( session_token ):
    #print(session_token)
    if session_token:
        try:
            decoded_claims = auth.verify_session_cookie(session_token, check_revoked=True)
            return decoded_claims
        except auth.InvalidSessionCookieError:
            # Session cookie is invalid, expired or revoked. Force user to login.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not logged in or Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else: #check Bearer
        bearer_scheme = HTTPBearer(auto_error=False)
        #print( bearer_scheme)
        return bearer_scheme

"""
def check_bearerToken():
    bearer_scheme = HTTPBearer(auto_error=False)
    print(bearer_scheme)
    decoded_claims = auth.verify_session_cookie(bearer_scheme.credentials, check_revoked=True)
    print( decoded_claims)
    return bearer_scheme
"""

def get_current_user(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """
    session cookie validation
    cred = { "scheme":"Bearer", "credentials":"...." }
    """
    #print(cred)
    try:
        decoded_token = auth.verify_session_cookie(cred.credentials)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    #print( decoded_token)
    user = decoded_token['firebase']['identities']
    user["id"] = decoded_token["user_id"]
    if "name" in decoded_token:
        user["name"] = decoded_token["name"]
    else :
        user["name"] = decoded_token["email"]

    #print(decoded_token)
    #print(user)

    return user


