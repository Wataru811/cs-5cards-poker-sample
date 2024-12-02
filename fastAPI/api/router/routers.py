from fastapi import APIRouter
import sys
sys.path.append("..")
from config.config import ROUTE_PREFIX_V1, ROUTE_PREFIX_V2
from . import (
    apiAuth,
    i18n,
    apiUser,
    poker,
)

##from .utils import router as translatorRouter

router = APIRouter()


def include_api_routes():
    router.include_router(apiAuth.router)
    router.include_router(i18n.router)
    router.include_router(apiUser.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(poker.router)

include_api_routes()


def test():
    return True


if __name__ == "__main__":
    test()