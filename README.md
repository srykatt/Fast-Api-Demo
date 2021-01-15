#### 启动项目
```shell script
uvicorn main:app --reload --host 0.0.0.0 --port 7999
# 帮助
uvicorn main:app --help | -h
```

#### 路由控制
通过 main.py add_router 添加路由


#### 需要修改
/Ad Editor/config/model_setting.bak -> /Ad Editor/config/model_setting.py
并设置为相对应的数据库

#### 生成数据库迁移文件
```shell script
 alembic revision --autogenerate -m "init commit"
```

#### 应用迁移文件
```shell script
alembic upgrade head
```