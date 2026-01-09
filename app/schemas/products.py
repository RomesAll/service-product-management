from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class ProductsPOSTSchemas(BaseModel):
    product: str
    type_product_id: int
    exist: bool
    provider: str
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
    type_product: str
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
    product_id: int
    price: float
    count_products: int
    model_config = ConfigDict(from_attributes=True)

class ProcurementGETSchemas(ProcurementPOSTSchemas):
    id: UUID
    created_at: datetime
    updated_at: datetime

class ProcurementPUTSchemas(ProcurementPOSTSchemas):
    id: UUID

class ProcurementRelSchemas(ProcurementPOSTSchemas):
    products: list["ProductsPOSTSchemas"]