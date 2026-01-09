from ..db.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Column
from sqlalchemy.dialects.postgresql import UUID

class ProcurementOrm(Base):
    __tablename__ = 'procurements'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='SET NULL'))
    price: Mapped[float]
    count_products: Mapped[int]
    product: Mapped["ProductsOrm"] = relationship(back_populates='procurements')

class TypeProduct(Base):
    __tablename__ = "type_products"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    type_product: Mapped[str] = mapped_column(nullable=False, unique=True)
    products: Mapped[list["ProductsOrm"]] = relationship(back_populates='type_product')

class ProductsOrm(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    product: Mapped[str] = mapped_column(nullable=False, unique=True)
    type_product_id: Mapped[int] = mapped_column(ForeignKey('type_products.id', ondelete='SET NULL'))
    exist: Mapped[bool] = mapped_column(default=False)
    provider: Mapped[str]
    procurements: Mapped[list["ProcurementOrm"]] = relationship(back_populates='product')
    type_product: Mapped["TypeProduct"] = relationship(back_populates='products')