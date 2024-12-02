from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    # get_redoc_html,
    get_swagger_ui_html,
    #get_swagger_ui_oauth2_redirect_html,
)
from router.routers import router
import platform
print("py version = " + platform.python_version())

import porker

print(porker.Card.cardAry)

origins = [
    "http://localhost:8000",
    "https://poker.interio-inc.com",
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

app.include_router(router)  



