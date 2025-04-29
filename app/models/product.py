from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func
from app.database.utils import Base

# 产品模型
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="产品名称")
    description = Column(String(255), nullable=True, comment="产品描述")
    price = Column(Float, nullable=False, comment="产品价格")
    in_stock = Column(Boolean, default=True, comment="是否有库存")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间") 