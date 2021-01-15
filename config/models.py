#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2021/1/4 16:25
# @Author : Srykatt

from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine, Text
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import List
import datetime
from .model_setting import Base
from sqlalchemy.orm import sessionmaker

__all__ = ['AdData']

class CreateAd(BaseModel):
    name: str
    image_url: str
    link: str
    country: str
    type: int  # 语言/国家 0/1


class AdData(Base):
    __tablename__ = 'ad_editor_data'
    create_time = Column('create_time', DateTime, default=datetime.datetime.now)  # 创建时间
    update_time = Column('update_time', DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now)  # 更新时间

    id = Column('id', Integer(), autoincrement=True, primary_key=True)
    code = Column('code', String(24), default='')  # code唯一标识
    name = Column('name', String(100), default='')  # 名称
    link = Column('link', Text(), default='')  # 链接
    type = Column('type', Integer(), default=0)  # 类型
    result_list = Column('country_list', Text(), default='')  # 国家|语言 列表
    upload_list = Column('upload_list', Text(), default='')  # 国家|语言 列表 -> 是否上传了图片
    status = Column('status', Integer(), default=0)  # 0/1 是否创建了资源
