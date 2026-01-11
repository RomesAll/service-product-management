__all__ = ('products_router', 'type_products_router', 'procurements_router', 'auth_router', 'users_router')
from .products import router as products_router
from .type_products import router as type_products_router
from .procurements import router as procurements_router
from .auth import router as auth_router
from .users import router as users_router