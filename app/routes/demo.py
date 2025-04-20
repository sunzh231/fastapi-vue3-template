from app import app
from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict

# 用于存储产品数据的内存字典
products_db: Dict[int, dict] = {}

# 用于生成产品ID的计数器
product_counter = 0

# 产品模型
class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    in_stock: bool = True

# 包含ID的产品模型
class ProductResponse(Product):
    id: int

# 产品更新模型
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    in_stock: Optional[bool] = None

@app.get('/api/products', response_model=List[ProductResponse], tags=['产品'])
def get_products():
    """获取所有产品列表"""
    return [{'id': id, **product} for id, product in products_db.items()]

@app.post('/api/products', response_model=ProductResponse, status_code=status.HTTP_201_CREATED, tags=['产品'])
def create_product(product: Product):
    """创建新产品"""
    global product_counter
    product_counter += 1
    product_id = product_counter
    
    # 存储产品信息
    products_db[product_id] = product.dict()
    
    # 返回创建的产品（包含ID）
    return {'id': product_id, **product.dict()}

@app.get('/api/products/{product_id}', response_model=ProductResponse, tags=['产品'])
def get_product(product_id: int):
    """获取指定ID的产品详情"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail=f'产品ID {product_id} 不存在')
    
    return {'id': product_id, **products_db[product_id]}

@app.put('/api/products/{product_id}', response_model=ProductResponse, tags=['产品'])
def update_product(product_id: int, product_update: ProductUpdate):
    """更新指定ID的产品"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail=f'产品ID {product_id} 不存在')
    
    # 获取当前产品数据
    current_product = products_db[product_id]
    
    # 只更新提供的字段
    update_data = product_update.dict(exclude_unset=True)
    updated_product = {**current_product, **update_data}
    
    # 保存更新后的数据
    products_db[product_id] = updated_product
    
    return {'id': product_id, **updated_product}

@app.delete('/api/products/{product_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['产品'])
def delete_product(product_id: int):
    """删除指定ID的产品"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail=f'产品ID {product_id} 不存在')
    
    # 从字典中删除该产品
    del products_db[product_id]
    
    # 204状态码无需返回内容
    return None

# 添加一些模拟数据
def init_sample_data():
    """初始化一些模拟产品数据"""
    sample_products = [
        Product(name="小米手机13", price=4999.00, description="最新的小米旗舰手机，搭载骁龙8 Gen 2处理器", in_stock=True),
        Product(name="MacBook Pro", price=12999.00, description="Apple高性能笔记本电脑，配备M2芯片", in_stock=True),
        Product(name="蓝牙耳机", price=299.00, description="无线蓝牙耳机，支持降噪功能", in_stock=True),
        Product(name="机械键盘", price=499.00, description="87键机械键盘，青轴，RGB背光", in_stock=False),
        Product(name="智能手表", price=1299.00, description="智能手表，支持心率监测、运动追踪等功能", in_stock=True),
    ]
    
    # 添加到产品数据库中
    for product in sample_products:
        create_product(product)
    
    print(f"已成功初始化 {len(sample_products)} 个模拟产品数据")

# 应用启动时初始化模拟数据
init_sample_data()
