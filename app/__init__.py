from fastapi import FastAPI
from dotenv import load_dotenv

from typing import Union
import os
import time

from fastapi import Depends
from typing import Annotated
from inertia import InertiaConfig, inertia_dependency_factory, Inertia
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from inertia import InertiaResponse, InertiaVersionConflictException, inertia_version_conflict_exception_handler
from app.configs.inertia_dependency import InertiaDep
from starlette.middleware.sessions import SessionMiddleware
import secrets

load_dotenv()

app = FastAPI()

# 添加 SessionMiddleware，使用随机密钥
app.add_middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(32))
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
app.mount("/assets", StaticFiles(directory=os.path.join(os.path.join(os.path.dirname(__file__), "..", "dist"), "assets")), name="assets")

app.add_exception_handler(InertiaVersionConflictException, inertia_version_conflict_exception_handler)


# 初始化数据库
from app.database.init import create_tables, init_sample_data

# 创建数据库表
create_tables()

# 添加短暂延迟，确保表已完全创
time.sleep(1)

# 导入路由
from app.routes import *

# 初始化示例数据
init_sample_data()
