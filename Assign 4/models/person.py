from sqlalchemy import Column, Integer, String
from werkzeug.security import check_password_hash
from models import db  # 从 models 包中导入 db 实例

class Person(db.Model):
    __tablename__ = 'persons'

    id = db.Column(Integer, primary_key=True, index=True)
    first_name = db.Column(String(50), nullable=False)
    last_name = db.Column(String(50), nullable=False)
    username = db.Column(String(50), unique=True, nullable=False)
    _Person__password = db.Column(String(255), nullable=False)  # 加密密码
    role = db.Column(String(50), nullable=False)  # 添加角色字段

    def __init__(self, first_name: str, last_name: str, username: str, password: str, role: str):
        """!
        Initializes the person with first name, last name, username, password, and role.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.__password = password  # 假设传入的密码已经加密
        self.role = role  # 初始化角色

    def get_full_name(self) -> str:
        """!
        Returns the full name of the person by concatenating the first and last name.
        """
        return f"{self.first_name} {self.last_name}"

    def check_password(self, password: str) -> bool:
        """!
        Checks if the provided password matches the stored hashed password.
        使用 werkzeug 的 check_password_hash 方法来验证密码。
        """
        return check_password_hash(self._Person__password, password)
    


    def __str__(self) -> str:
        """!
        Returns a string representation of the person.
        """
        return f"Name: {self.get_full_name()}, Username: {self.username}, Role: {self.role}"
