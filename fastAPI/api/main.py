from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    # get_redoc_html,
    get_swagger_ui_html,
    #get_swagger_ui_oauth2_redirect_html,
)
from router.routers import router
import platform
import asyncio
import grpc

from api.grpc.poker import start_grpc_server
from api.poker.card import Card
from api.poker.rule5cd import rulePoker
#import sys
#sys.path.append('./')
#from api.pb import poker_pb2
#from api.pb import poker_pb2_grpc

# --- test ---


print("py version = " + platform.python_version())
rule = rulePoker()
result = rule.checkHandPid([0,27,28,29,30])
print(result.__dict__)
result = rule.checkHandPid([0,13,26,29,30])
print(result.__dict__)
result = rule.checkHandPid([0,13,26,39,30])
print(result.__dict__)
result = rule.checkHandPid([4,13,26,39,30])
print(result.__dict__)
result = rule.checkHandPid([1,27,26,43,30])
print(result.__dict__)






origins = [
    "http://localhost:8000",
    "https://poker-dev.interio-inc.com",
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
@app.get("/")
async def root():
    return {"message": "Hello World"}
"""

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )



# gRPC サーバーと FastAPI の統合
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_grpc_server())

app.include_router(router)  