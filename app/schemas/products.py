from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID

class ProductsPOSTSchemas(BaseModel):
    product: str = Field(default=None)
    type_product_id: int = Field(default=None)
    exist: bool = Field(default=None)
    provider: str = Field(default=None)
    model_config = ConfigDict(from_attributes=True)

class ProductsGETSchemas(ProductsPOSTSchemas):
    id: int
    created_at: datetime
    updated_at: datetime

class ProductsPUTSchemas(ProductsPOSTSchemas):
    id: int

class ProductsRelSchemas(ProductsPOSTSchemas):
    procurements: list["ProcurementPOSTSchemas"]
    type_product: "TypeProductPOSTSchemas"

class TypeProductPOSTSchemas(BaseModel):
    type_product: str = Field(default=None)
    model_config = ConfigDict(from_attributes=True)

class TypeProductGETSchemas(TypeProductPOSTSchemas):
    id: int
    created_at: datetime
    updated_at: datetime

class TypeProductPUTSchemas(TypeProductPOSTSchemas):
    id: int

class TypeProductRelSchemas(TypeProductPOSTSchemas):
    products: list["ProductsPOSTSchemas"]

class ProcurementPOSTSchemas(BaseModel):
    product_id: int = Field(default=None)
    price: float = Field(default=None)
    count_products: int = Field(default=None)
    model_config = ConfigDict(from_attributes=True)

class ProcurementGETSchemas(ProcurementPOSTSchemas):
    id: UUID
    created_at: datetime
    updated_at: datetime

class ProcurementPUTSchemas(ProcurementPOSTSchemas):
    id: UUID

class ProcurementRelSchemas(ProcurementPOSTSchemas):
    products: list["ProductsPOSTSchemas"]