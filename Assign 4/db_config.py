from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库连接 URL
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/fresh_harvest"

# 创建引擎
engine = create_engine(DATABASE_URL)

# 创建一个会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类，所有的模型都将继承这个基类
Base = declarative_base()
