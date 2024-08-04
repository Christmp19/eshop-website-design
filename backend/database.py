from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion à la base de données SQLite
DATABASE_URL = "sqlite:///./test.db"

# Crée l'engine SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crée une session pour les transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Déclare la base pour les modèles
Base = declarative_base()