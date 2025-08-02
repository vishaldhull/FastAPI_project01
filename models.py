from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String)
    role = Column(String)  # Default role can be 'user', 'admin', etc.
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        return f"<Todo id={self.id} title={self.title} complete={self.complete}>"