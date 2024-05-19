from config import db, app
from models.storage import User, BookMarks

def initialize_database():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    initialize_database()