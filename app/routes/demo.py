from app import app
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

# 导入数据库依赖
from app.database.utils import get_db
from app.models import ProductModel
from app.schemas import ProductCreate, Product, ProductUpdate

@app.get('/api/products', response_model=list[Product], tags=['产品'])
def get_products(db: Session = Depends(get_db)):
    """获取所有产品列表"""
    products = db.query(ProductModel).all()
    return products

@app.post('/api/products', response_model=Product, status_code=status.HTTP_201_CREATED, tags=['产品'])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """创建新产品"""
    # 创建数据库模型实例
    db_product = ProductModel(
        name=product.name,
        price=product.price,
        description=product.description,
        in_stock=product.in_stock
    )
    
    # 添加到数据库
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # 返回创建的产品
    return db_product

@app.get('/api/products/{product_id}', response_model=Product, tags=['产品'])
def get_product(product_id: int, db: Session = Depends(get_db)):
    """获取指定ID的产品详情"""
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail=f'产品ID {product_id} 不存在')
    
    return db_product

@app.put('/api/products/{product_id}', response_model=Product, tags=['产品'])
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    """更新指定ID的产品"""
    # 查询产品
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail=f'产品ID {product_id} 不存在')
    
    # 只更新提供的字段
    update_data = product_update.model_dump(exclude_unset=True)
    
    # 应用更新
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    # 保存更新
    db.commit()
    db.refresh(db_product)
    
    return db_product

@app.delete('/api/products/{product_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['产品'])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """删除指定ID的产品"""
    # 查询产品
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail=f'产品ID {product_id} 不存在')
    
    # 从数据库中删除该产品
    db.delete(db_product)
    db.commit()
    
    # 204状态码无需返回内容
    return None

# 注：示例数据初始化已移至 db_init.py 文件
