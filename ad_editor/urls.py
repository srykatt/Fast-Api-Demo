#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2021/1/12 15:02
# @Author : Srykatt

from fastapi import APIRouter, Response
from pydantic import BaseModel
from ad_editor.untils.response_code import *
from ad_editor.web_views.ad_info import get_code, search_ad, create_ad
from ad_editor.web_views.upload import upload_img

# 路由管理页面
ad_editor_router = APIRouter()
# ---------------    WEB  -----------
ad_editor_router.add_api_route(methods=['GET'], path='/{version}/web/get/code', endpoint=get_code,
                               summary='获取code')  # 获取Code
ad_editor_router.add_api_route(methods=['POST'], path='/{version}/web/upload', endpoint=upload_img,
                               summary='上传图片')  # 上传图片接口
ad_editor_router.add_api_route(methods=['POST'], path='/{version}/web/create/ad', endpoint=create_ad,
                               summary='创建广告')  # 创建广告
ad_editor_router.add_api_route(methods=['GET'], path='/{version}/web/search/ad', endpoint=search_ad,
                               summary='查询广告')  # 查询广告
