from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 从环境变量中获取数据库连接信息
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/product_db")

# 创建 SQLAlchemy 引擎
engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类模型
Base = declarative_base()

# 依赖项函数，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
