from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 产品基础模型
class ProductBase(BaseModel):
    name: str = Field(..., description="产品名称")
    description: Optional[str] = Field(None, description="产品描述")
    price: float = Field(..., ge=0, description="产品价格")
    stock: int = Field(0, ge=0, description="库存数量")

# 创建产品请求模型
class ProductCreate(ProductBase):
    pass

# 更新产品请求模型
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, description="产品名称")
    description: Optional[str] = Field(None, description="产品描述")
    price: Optional[float] = Field(None, ge=0, description="产品价格")
    stock: Optional[int] = Field(None, ge=0, description="库存数量")

# 产品响应模型
class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
