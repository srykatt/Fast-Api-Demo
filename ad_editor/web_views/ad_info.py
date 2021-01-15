#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2021/1/12 15:00
# @Author : Srykatt
from ad_editor.untils.response_code import *
from pydantic import BaseModel, AnyHttpUrl
from typing import Optional


async def get_code(*, request: Response):
    session = db()
    while True:
        code = ''.join(random.sample(string.ascii_uppercase + string.digits, 6))
        if not session.query(exists().where(models.AdData.code == code)).scalar():
            break
        else:
            code = ''.join(random.sample(string.ascii_uppercase + string.digits, 6))
    code_dict = {'code': code}
    ad_data = models.AdData(
        code=code
    )
    session.add(ad_data)
    session.commit()
    return resp_200(data=code_dict)


class Item(BaseModel):
    name: str
    code: str
    link: AnyHttpUrl


async def create_ad(*, item: Item):
    print(item.dict())
    session = db()
    if session.query(exists().where(models.AdData.code == item.code)).scalar():
        # 如果code存在
        ad_obj = session.query(models.AdData).filter(models.AdData.code == item.code).first()
        ad_obj.name = item.name
        ad_obj.link = item.link
        session.commit()
    return resp_200(data=[])


async def search_ad(*, ad_type: int = None, code_list: Optional[str] = None, page: int = 1, size: int = 20):
    session = db()
    ad_obj = session.query(models.AdData)
    if ad_type:
        ad_obj = ad_obj.filter_by(type=ad_type)
    if code_list:
        code_list = code_list.split(',')
        ad_obj = ad_obj.filter(and_(
            or_(~models.AdData.code.in_(code_list))
        ))
    ad_obj = ad_obj.order_by(models.AdData.create_time.desc())
    count = ad_obj.count()
    return_list = [
                      {
                          'name': obj.name,
                          'link': obj.link,
                          'code': obj.code,
                          'upload_list': obj.upload_list,
                          'status': obj.status,
                          'create_time': str(obj.create_time),
                          'type': obj.type,
                      }
                      for obj in ad_obj
                  ][(page - 1) * size: page * size]
    return_data = {'ad_list': return_list, 'count': count}
    return resp_200(data=return_data)
