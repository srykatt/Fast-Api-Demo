# -*- coding: utf-8 -*-
# @Time   : 2021/1/12 16:58
# @Author : Srykatt
from ad_editor.untils.response_code import *
from ad_editor.untils.admin_settings import *
from enum import Enum


class AdTypeEnum(Enum):
    country = 1
    language = 2


async def upload_img(*, file: UploadFile = File(...), code: str, ad_type: int, value: str):
    session = db()
    save_dir = f"{settings.BASE_DIR}/upload"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    ad_type_id = ad_type
    ad_type = AdTypeEnum(ad_type).name
    file_name = f'{code}-{ad_type}-{value}'
    url = f'ad_editor/{code}'
    flag = upload(file, url, file_name=file_name)

    if not session.query(exists().where(models.AdData.code == code)).scalar():
        # 传入的 code 不存在的
        ad_data = models.AdData(
            code=code,
            type=ad_type_id,
        )
        session.add(ad_data)
        session.commit()
    if flag:
        upload_list_exists = session.query(models.AdData).filter_by(code=code).first()
        if check_value_in_upload_list(upload_list_exists, value):
            # 先查询是否存在已上传的列表里面，如果存在就先把它干掉
            del_sql_value(upload_list_exists, session, value)

    ad_data = session.query(models.AdData).filter_by(code=code).first()
    ad_data.upload_list += (value + ',')
    ad_data.type = ad_type_id,
    if check_finish_status:
        ad_data.status = 1
    session.commit()
    return resp_200(data=[])


def upload(file, url, base_dir=None, file_name=None, *args, **kwargs):
    base_dir = base_dir if base_dir else f"{settings.BASE_DIR}/upload/" + str(uuid.uuid4())
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    if not file_name:
        file_name = file.name
    f = open(base_dir + os.sep + file_name, 'wb')
    for chunk in file.file:
        f.write(chunk)
    f.close()
    flag = do_upload(file_name, url, base_dir, args, kwargs)
    shutil.rmtree(base_dir)
    return flag


def do_upload(file_name, url, base_dir=None, *args, **kwargs):
    flag = 0
    # if file_name.split('.')[-1] == 'zip':
    #     flag = upload_zip(file_name, url, base_dir, flag, args, kwargs)
    # if file_name.split('.')[-1] == 'webp':
    auth = oss2.Auth(ADMIN_AK, ADMIN_SK)
    for bucket_config in bucket_list.values():
        bucket = oss2.Bucket(auth, 'http://%s' % bucket_config.get('endpoint'), bucket_config.get('name'))
        # file_path, bucket, url, base_root, return_flag
        flag = upload_simple_file(file_name, bucket, url, base_dir, flag)
    return flag


def upload_simple_file(file_path, bucket, url, base_root, return_flag):
    file_path = base_root + os.sep + file_path
    relative_path = file_path.split(base_root)[1]
    flag = True
    max_retry = 5
    while flag and max_retry > 0:
        print(flag)
        try:
            # pass
            print(url + relative_path, )
            bucket.put_object_from_file(url + relative_path, file_path)
        except Exception as e:
            print(e)
            return_flag = 0
            max_retry -= 1
        else:
            return_flag = 1
            flag = False
            print('upload success')
    return return_flag


def check_value_in_upload_list(sql_obj, value):
    # 检查国家是否已上传过
    if value in sql_obj.upload_list.split(','):
        return True
    return False


def del_sql_value(sql_obj, session, value=None):
    # 删除已上传的国家
    sql_obj_list: list = (sql_obj.upload_list.split(','))
    sql_obj_list = [obj for obj in sql_obj_list if obj != value]
    sql_obj.upload_list = ','.join(sql_obj_list)
    session.commit()
    return True


def check_finish_status(sql_obj):
    pass
