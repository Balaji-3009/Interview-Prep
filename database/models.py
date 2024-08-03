from sqlalchemy import Column, ForeignKey, Integer, String, JSON, Boolean, Date, TIME, DateTime, func
from database.session import Base
from sqlalchemy.orm import relationship

class Users(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key= True, index= True)
    email = Column(String)
    password = Column(String)
    
    qna = relationship("QnA", back_populates='user')

class QnA(Base):
    
    __tablename__ = 'qna'
    id = Column(Integer, primary_key= True, index= True)
    userId = Column(Integer, ForeignKey("users.id"))
    sessionId = Column(Integer)
    question = Column(String)
    answer = Column(String)
    
    user = relationship("Users", back_populates='qna')