from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

db = SQLAlchemy()

client = MongoClient()

mongo_db = client['present_ai']

p_sessions = mongo_db['presentation_sessions']
"""
p_sessions schema:
{
    user_id: uuid
    presentation_id: uuid
    name: string
    description: string
    length: number
}
"""
