#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2021/1/4 16:10
# @Author : Srykatt

from typing import Optional
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter
from ad_editor.urls import ad_editor_router

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse

from ad_editor.untils.response_code import resp_200, resp_400

app = FastAPI()
app.debug = True
app.title = 'Ad Editor'
app.description = '这是Ad Editor API文档'
app.version = '1.0.0'

origins = ["http://192.168.50.3", 'http://192.168.50.193','http://127.0.0.1']  # 也可以设置为"*"，即为所有。

api_router = APIRouter()
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex='https?://.*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ad_editor_router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # return PlainTextResponse(str(exc), status_code=400)
    return resp_400(msg=str(exc).strip(), data=[])
