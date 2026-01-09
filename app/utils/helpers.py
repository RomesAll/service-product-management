from ..db.database import session_maker
from ..core import settings

def get_session():
    try:
        session = session_maker()
        yield session
    except Exception as e:
        settings.logger.error(e)
        session.rollback()
    finally:
        session.close()