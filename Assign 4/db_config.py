from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 数据库连接 URL
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/fresh_harvest12"

# 创建引擎
engine = create_engine(DATABASE_URL)

# 创建一个会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
