from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Float
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, unique=True, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Order(Base):
    __tablename__ = "orders"

    # STATUS_CHOICES = (
    #    ("PENDENTE", "Pendente"),
    #    ("CANCELADO", "Cancelado"),
    #    ("FINALIZADO", "Finalizado")
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    user_id = Column("user", Integer, ForeignKey("users.id"))
    price = Column("price", Float)

    def __init__(self, user_id, status="PENDENTE", price=0):
        self.user_id = user_id
        self.status = status
        self.price = price


class ItemOrder(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer)
    flavor = Column("flavor", String)
    size = Column("size", String)
    price = Column("price", Float)
    price_unit = Column("price_unit", String)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))

    def __init__(self, user_id, quantity, size, price, price_unit, order_id):
        self.user_id = user_id
        self.quantity = quantity
        self.size = size
        self.price = price
        self.price_unit = price_unit
        self.order_id = order_id
