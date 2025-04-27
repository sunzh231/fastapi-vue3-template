from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.models.base import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="产品名称")
    description = Column(String(255), nullable=True, comment="产品描述")
    price = Column(Float, nullable=False, comment="产品价格")
    stock = Column(Integer, default=0, comment="库存数量")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
