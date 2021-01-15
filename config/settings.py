#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2021/1/11 09:44
# @Author : Srykatt
import os
from pydantic import BaseSettings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    SECRET_KEY: str = "(-ASp+_SC?ZX)-Ulhw0848hnvVG-iqKyJSD&*&^-H3C9mqEqSl8KN-YRzRE"


settings = Settings()

