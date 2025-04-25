from app.database.utils import engine, SessionLocal, Base
from app.models.base import ProductModel
from app.schemas.base import ProductCreate

# 初始化数据库表
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("数据库表已创建")

# 初始化示例数据
def init_sample_data():
    # 创建数据库会话
    db = SessionLocal()
    
    # 检查是否已有产品数据
    products_count = db.query(ProductModel).count()
    if products_count > 0:
        print(f"数据库中已有 {products_count} 个产品记录，跳过初始化示例数据")
        db.close()
        return
    
    # 示例产品数据
    sample_products = [
        ProductCreate(name="小米手机13", price=4999.00, description="最新的小米旗舰手机，搭载骨龙 8 Gen 2处理器", in_stock=True),
        ProductCreate(name="MacBook Pro", price=12999.00, description="Apple高性能笔记本电脑，配备M2芯片", in_stock=True),
        ProductCreate(name="蓝牙耳机", price=299.00, description="无线蓝牙耳机，支持降噪功能", in_stock=True),
        ProductCreate(name="机械键盘", price=499.00, description="87键机械键盘，青轴，RGB背光", in_stock=False),
        ProductCreate(name="智能手表", price=1299.00, description="智能手表，支持心率监测、运动追踪等功能", in_stock=True),
    ]
    
    # 添加产品到数据库
    for product_data in sample_products:
        product = ProductModel(
            name=product_data.name,
            price=product_data.price,
            description=product_data.description,
            in_stock=product_data.in_stock
        )
        db.add(product)
    
    # 提交更改
    db.commit()
    db.close()
    
    print(f"已成功初始化 {len(sample_products)} 个示例产品数据")
