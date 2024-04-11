from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

db = SQLAlchemy()

client = MongoClient()

mongo_db = client['present_ai']

p_sessions = mongo_db['presentation_sessions']
"""
p_sessions schema:
{
    id: uuid
    name: string
    length: number
}
"""
