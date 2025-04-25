from pydantic import BaseModel
from typing import Optional, List

# 产品基础模型
class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    in_stock: bool = True

# 创建产品模型
class ProductCreate(ProductBase):
    pass

# 产品更新模型
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    in_stock: Optional[bool] = None

# 产品返回模型
class Product(ProductBase):
    id: int
    
    class Config:
        # 启用ORM模式，允许从ORM对象直接创建Pydantic模型
        orm_mode = True
        # SQLAlchemy 2.0 兼容
        from_attributes = True
