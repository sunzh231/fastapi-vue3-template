from app import app
from app.configs.inertia_dependency import InertiaDep
from inertia import InertiaResponse
from fastapi import Depends, HTTPException, status, Query
from app.database.utils import get_db
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from typing import List, Optional
from datetime import datetime
import json

# 自定义JSON编码器，处理datetime对象
def custom_json_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

# 序列化数据的辅助函数
def serialize_model(model_data):
    if isinstance(model_data, list):
        return json.loads(json.dumps([m.model_dump() for m in model_data], default=custom_json_encoder))
    return json.loads(json.dumps(model_data.model_dump(), default=custom_json_encoder))

# 获取所有产品
@app.get('/products', response_model=None)
async def get_products(
    inertia: InertiaDep,
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None, description="搜索产品名称"),
    page: int = Query(1, ge=1, description="页码"),
    per_page: int = Query(10, ge=1, le=100, description="每页数量")
) -> InertiaResponse:
    # 构建查询
    query = db.query(Product)
    
    # 处理搜索
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    
    # 计算总数量
    total = query.count()
    
    # 分页处理
    offset = (page - 1) * per_page
    products = query.offset(offset).limit(per_page).all()
    
    # 将产品数据转换为Pydantic模型并进行自定义序列化
    products_data = [ProductResponse.model_validate(product) for product in products]
    serialized_products = serialize_model(products_data)
    
    return await inertia.render('Products/Index', {
        'products': serialized_products,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total
        },
        'search': search or ''
    })

# 创建产品页面
@app.get('/products/create', response_model=None)
async def create_product_page(
    inertia: InertiaDep
) -> InertiaResponse:
    return await inertia.render('Products/Create', {})

# 获取单个产品
@app.get('/products/{product_id}', response_model=None)
async def get_product(
    product_id: int,
    inertia: InertiaDep,
    db: Session = Depends(get_db)
) -> InertiaResponse:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="产品不存在")
    
    # 将产品数据转换为Pydantic模型并进行自定义序列化
    product_data = ProductResponse.model_validate(product)
    serialized_product = serialize_model(product_data)
    
    return await inertia.render('Products/Detail', {
        'product': serialized_product
    })

# 创建产品
@app.post('/products', response_model=None)
async def create_product(
    inertia: InertiaDep,
    product_data: ProductCreate,
    db: Session = Depends(get_db)
) -> InertiaResponse:
    # 创建产品
    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        in_stock=True
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    
    # 使用 Inertia 重定向到产品列表页
    return await inertia.location('/products')

# 编辑产品页面
@app.get('/products/{product_id}/edit', response_model=None)
async def edit_product_page(
    product_id: int,
    inertia: InertiaDep,
    db: Session = Depends(get_db)
) -> InertiaResponse:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="产品不存在")
    
    # 将产品数据转换为Pydantic模型并进行自定义序列化
    product_data = ProductResponse.model_validate(product)
    serialized_product = serialize_model(product_data)
    
    return await inertia.render('Products/Edit', {
        'product': serialized_product
    })

# 更新产品
@app.put('/products/{product_id}', response_model=None)
async def update_product(
    product_id: int,
    inertia: InertiaDep,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
) -> InertiaResponse:
    # 查找产品
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="产品不存在")
    
    # 更新产品数据
    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    
    # 使用 Inertia 重定向到产品列表页
    return await inertia.location('/products')

# 删除产品
@app.delete('/products/{product_id}', response_model=None)
async def delete_product(
    product_id: int,
    inertia: InertiaDep,
    db: Session = Depends(get_db)
) -> InertiaResponse:
    # 查找产品
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="产品不存在")
    
    # 删除产品
    db.delete(product)
    db.commit()
    
    # 使用 Inertia 重定向到产品列表页
    return await inertia.location('/products') 