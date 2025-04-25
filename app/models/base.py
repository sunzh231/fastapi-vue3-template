from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from app.database.utils import Base

# 产品数据库模型
class ProductModel(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    in_stock = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Product {self.name}>"
