from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    limit: int = Field(default=50, ge=0, le=1000, description="Limit the number of results")
    offset: int = Field(default=0, ge=0, description="Offset for the results")

