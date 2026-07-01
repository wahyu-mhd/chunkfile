from app.database import Base, engine
from app import models  # noqa: F401


def main():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")


if __name__ == "__main__":
    main()