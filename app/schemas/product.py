from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import json

# 产品基础模型
class ProductBase(BaseModel):
    name: str = Field(..., description="产品名称")
    description: Optional[str] = Field(None, description="产品描述")
    price: float = Field(..., ge=0, description="产品价格")
    in_stock: bool = Field(True, description="是否有库存")
    
    model_config = {
        "from_attributes": True
    }

# 创建产品请求模型
class ProductCreate(ProductBase):
    pass

# 更新产品请求模型
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, description="产品名称")
    description: Optional[str] = Field(None, description="产品描述")
    price: Optional[float] = Field(None, ge=0, description="产品价格")
    in_stock: Optional[bool] = Field(None, description="是否有库存")
    
    model_config = {
        "from_attributes": True
    }

# 产品响应模型
class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None
        }
    }
