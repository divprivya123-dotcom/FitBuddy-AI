from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def init_db():
    """Create database tables when the application starts."""
    from app.models import Base

    Base.metadata.create_all(bind=engine)
    with engine.begin() as connection:
        columns = connection.exec_driver_sql("PRAGMA table_info(users)").fetchall()
        column_names = {column[1] for column in columns}
        if "feedback" not in column_names:
            connection.exec_driver_sql(
                "ALTER TABLE users ADD COLUMN feedback TEXT NOT NULL DEFAULT ''"
            )


def save_user(user):
    db = SessionLocal()
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


def get_user(user_id):
    from app.models import User

    db = SessionLocal()
    try:
        return db.query(User).filter(User.user_id == user_id).first()
    finally:
        db.close()


def get_all_users():
    from app.models import User

    db = SessionLocal()
    try:
        return db.query(User).order_by(User.id.desc()).all()
    finally:
        db.close()


def update_plan(user_id, updated_plan, feedback=""):
    from app.models import User

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.updated_plan = updated_plan
            user.feedback = feedback
            db.commit()
            db.refresh(user)
        return user
    finally:
        db.close()