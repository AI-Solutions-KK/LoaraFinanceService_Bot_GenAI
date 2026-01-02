# create_db.py
from db.base import Base
from db.config import engine

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
