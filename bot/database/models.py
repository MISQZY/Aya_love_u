from sqlalchemy import Column, Integer, String, ForeignKey
from database.connection import Base
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator
import json

class JsonArray(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=False)
    name = Column(String, nullable=True)
    diminutive_affectionate_list = Column(JsonArray, nullable=True)

    user_config_id = Column(Integer, ForeignKey('user_config.id'), nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username}, name={self.name}, diminutive_affectionate_list={self.diminutive_affectionate_list})>"

class UserConfig(Base):
    __tablename__ = "user_config"

    id = Column(Integer, primary_key=True)
    time_zone_id = Column(Integer, ForeignKey('timezone.id'), nullable=False)
    week_type_id = Column(Integer, ForeignKey('weektype.id'), nullable=False)

    def __repr__(self):
        return f"<UserConfig(id={self.id}, time_zone_id={self.time_zone_id}, week_type_id={self.week_type_id})>"

# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True)
#     telegram_id = Column(Integer, unique=True, nullable=False)
#     username = Column(String, nullable=False)
#     name = Column(String, nullable=True)
#     diminutive_affectionate_list = Column(JsonArray,nullable=True)

#     user_configs = relationship('UserConfig', secondary='user_configs', back_populates='users', cascade='all, delete-orphan')
    
#     def __repr__(self):
#         return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username}, name={self.name}, diminutive_affectionate_list={self.diminutive_affectionate_list})>"

# class UserConfig(Base):
#     __tablename__ = "user_config"

#     id = Column(Integer, primary_key=True)
#     time_zone_id = Column(Integer, ForeignKey('timezone.id'), nullable=False)
#     week_type_id = Column(Integer, ForeignKey('weektype.id'), nullable=False)

#     users = relationship('User', secondary='user_configs', back_populates='user_configs')

#     def __repr__(self):
#         return f"<Timezone(id={self.id}, time_zone_id={self.time_zone_id}, week_type_id={self.week_type_id})>"

# class UserConfigs(Base):
#     __tablename__ = 'user_configs'

#     user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
#     user_config_id = Column(Integer, ForeignKey('user_config.id'), primary_key=True)

class Timezone(Base):
    __tablename__ = 'timezone'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Timezone(id={self.id}, name={self.name})>"

class Weektype(Base):
    __tablename__ = 'weektype'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Weektype(id={self.id}, name={self.name})>"