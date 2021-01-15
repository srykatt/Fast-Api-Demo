#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2021/1/12 14:11
# @Author : Srykatt

# system import
import random
import string
import os
import sys
import uuid
import shutil
import json

# fast_api import
from config import settings
from fastapi import status, UploadFile, File
from config.model_setting import SessionLocal as db
from starlette.requests import Request
from fastapi.responses import JSONResponse, Response  # , ORJSONResponse
from typing import Union
from sqlalchemy import exists, and_, or_
from config import models
import datetime

# other import
import oss2


# 注意有个 * 号 不是笔误， 意思是调用的时候要指定参数 e.g.resp_200（data=xxxx)
def resp_200(*, data: Union[list, dict, str]) -> Response:
    return Response(
        headers={'Accept': '*/*',

                 },
        status_code=status.HTTP_200_OK,
        media_type='application/json',
        content=
        json.dumps({
            'code': 200,
            'msg': "操作成功",
            'data': data,
        })
    )


def resp_400(*, data: str = None, msg: str = "操作失败") -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'code': 400,
            'msg': msg,
            'data': data,
        }
    )

# 所有响应状态都封装在这里
