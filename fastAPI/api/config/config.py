from typing import List
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

###
# Properties configurations
###

ROUTE_PREFIX_V1 = "/api/v1"
ROUTE_PREFIX_V2 = "/api/v2"


"""
API_PREFIX = "/api"

JWT_TOKEN_PREFIX = "Authorization"

config = Config(".env")

ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)

ALLOWED_ORIGINS = [
    "http://localhost:8081",
    "https://spec-api.interio-inc.com",
    "https://spec.interio-inc.com",
]
"""