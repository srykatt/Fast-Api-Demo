#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2021/1/13 09:29
# @Author : Srykatt
# coding: utf-8


from pycountry_convert import country_alpha2_to_continent_code as ccc

# [AF]非洲, [EU]欧洲, [AS]亚洲, [OA]大洋洲, [NA]北美洲, [SA]南美洲, [AN]南极洲
ADMIN_AK = ''

CN_BUCKET = ''

cn_endpoint = ''

cn_region = ''

# bucket 配置
bucket_list = {
    'cn_bucket': {'name': CN_BUCKET, 'endpoint': cn_endpoint, 'region': cn_region, 'country': 'cn'},
    # 'us_bucket': {'name': US_BUCKET, 'endpoint': us_endpoint, 'region': us_region, 'country': 'us'},
    # 'eu_bucket': {'name': EU_BUCKET, 'endpoint': eu_endpoint, 'region': eu_region, 'country': 'eu'},
}

country_to_bucket = [
    {'AS': bucket_list.get('cn_bucket')},
    # {'OA': bucket_list.get('cn_bucket')},
    # {'NA': bucket_list.get('us_bucket')},
    # {'SA': bucket_list.get('us_bucket')},
    # {'EU': bucket_list.get('eu_bucket')},
    # {'AF': bucket_list.get('eu_bucket')},
    # {'AN': bucket_list.get('us_bucket')},
]


def get_bucket_config(country=False):
    if country and isinstance(country, str):
        country = country.upper()
        try:
            continent = ccc(country)
        except Exception as e:
            print(e)
            continent = 'AS'
        for config in country_to_bucket:
            if config.get(continent, False):
                return config.get(continent)
    return bucket_list.get('cn_bucket')


def get_region_config(bucket):
    return [config['region'] for config in bucket_list.values() if config['name'] == bucket][0]
