from app.core.database import engine, Base
from app.models import test_connection

Base.metadata.create_all(bind=engine)
