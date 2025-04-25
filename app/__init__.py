from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# 初始化数据库
from app.database.init import create_tables, init_sample_data

# 创建数据库表
create_tables()

# 导入路由
from app.routes import *

# 初始化示例数据
init_sample_data()
