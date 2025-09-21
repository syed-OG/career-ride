from app import app, db
from models import User, Profile
from sqlalchemy import text

def migrate_database():
    """Add new columns to Profile and User tables."""
    with app.app_context():
        # Create columns in the User model
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS reset_token VARCHAR(100)'))
            conn.execute(text('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS reset_token_expiration TIMESTAMP'))
            
            # Create columns in the Profile model
            conn.execute(text('ALTER TABLE profile ADD COLUMN IF NOT EXISTS areas_of_interest TEXT'))
            conn.execute(text('ALTER TABLE profile ADD COLUMN IF NOT EXISTS career_objective TEXT'))
            conn.execute(text('ALTER TABLE profile ADD COLUMN IF NOT EXISTS extracurricular_activities TEXT'))
            conn.execute(text('ALTER TABLE profile ADD COLUMN IF NOT EXISTS certifications TEXT'))
            conn.execute(text('ALTER TABLE profile ADD COLUMN IF NOT EXISTS secondary_education VARCHAR(256)'))
            conn.execute(text('ALTER TABLE profile ADD COLUMN IF NOT EXISTS higher_education VARCHAR(256)'))
            conn.execute(text('ALTER TABLE profile ADD COLUMN IF NOT EXISTS languages_known TEXT'))
            conn.execute(text('ALTER TABLE profile ADD COLUMN IF NOT EXISTS twitter_url VARCHAR(128)'))
            conn.execute(text('ALTER TABLE profile ADD COLUMN IF NOT EXISTS instagram_url VARCHAR(128)'))
            conn.execute(text('ALTER TABLE profile ADD COLUMN IF NOT EXISTS profile_picture VARCHAR(256)'))
            
            conn.commit()
        
        print("Migration completed successfully.")

if __name__ == "__main__":
    migrate_database()