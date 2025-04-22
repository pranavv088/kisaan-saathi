from pymongo import MongoClient
from bson import ObjectId
from config import Config
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        try:
            self.client = MongoClient(Config.MONGODB_URI)
            # Test the connection
            self.client.admin.command('ping')
            self.db = self.client[Config.MONGODB_DB]
            self._create_indexes()
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    def _create_indexes(self):
        try:
            for collection_name, indexes in Config.INDEXES.items():
                collection = self.db[collection_name]
                for index in indexes:
                    collection.create_index(index["key"], unique=index.get("unique", False))
            logger.info("MongoDB indexes created successfully")
        except Exception as e:
            logger.error(f"Failed to create indexes: {str(e)}")
            raise

    def get_user(self, user_id):
        try:
            return self.db[Config.USERS_COLLECTION].find_one({"_id": ObjectId(user_id)})
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return None

    def get_user_by_email(self, email):
        try:
            return self.db[Config.USERS_COLLECTION].find_one({"email": email})
        except Exception as e:
            logger.error(f"Error getting user by email: {str(e)}")
            return None

    def create_user(self, user_data):
        try:
            user_data["created_at"] = datetime.utcnow()
            result = self.db[Config.USERS_COLLECTION].insert_one(user_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return None

    def update_user(self, user_id, updates):
        try:
            updates["updated_at"] = datetime.utcnow()
            result = self.db[Config.USERS_COLLECTION].update_one(
                {"_id": ObjectId(user_id)},
                {"$set": updates}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            return False

    def save_disease_record(self, user_id, image_path, prediction):
        try:
            record = {
                "user_id": ObjectId(user_id),
                "image_path": image_path,
                "prediction": prediction,
                "date": datetime.utcnow()
            }
            self.db[Config.DISEASE_COLLECTION].insert_one(record)
            return True
        except Exception as e:
            logger.error(f"Error saving disease record: {str(e)}")
            return False

    def get_user_disease_records(self, user_id):
        try:
            return list(self.db[Config.DISEASE_COLLECTION].find(
                {"user_id": ObjectId(user_id)},
                sort=[("date", -1)]
            ))
        except Exception as e:
            logger.error(f"Error getting disease records: {str(e)}")
            return []

    def save_weather_data(self, location, weather_data):
        try:
            record = {
                "location": location,
                "data": weather_data,
                "date": datetime.utcnow()
            }
            self.db[Config.WEATHER_COLLECTION].insert_one(record)
            return True
        except Exception as e:
            logger.error(f"Error saving weather data: {str(e)}")
            return False

    def get_crop_info(self, crop_name):
        try:
            return self.db[Config.CROPS_COLLECTION].find_one({"name": crop_name})
        except Exception as e:
            logger.error(f"Error getting crop info: {str(e)}")
            return None

    def close(self):
        if self.client:
            self.client.close()

    def get_developers(self):
        """Get all developers from the database"""
        return list(self.db.developers.find())

    def get_developer(self, developer_id):
        """Get a specific developer by ID"""
        try:
            return self.db.developers.find_one({"_id": ObjectId(developer_id)})
        except:
            return None

    def create_developer(self, developer_data):
        """Create a new developer profile"""
        try:
            result = self.db.developers.insert_one(developer_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating developer: {str(e)}")
            return None

    def update_developer(self, developer_id, updates):
        """Update a developer's profile"""
        try:
            result = self.db.developers.update_one(
                {"_id": ObjectId(developer_id)},
                {"$set": updates}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating developer: {str(e)}")
            return False

# Create a global database instance
db = Database() 