from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import Flask


load_dotenv('C:/Users/bonni/OneDrive/Documents/monsterhunterrisebuilds/.env')

MONGODB_URI = os.getenv('MONGODB_URI')

client = MongoClient(MONGODB_URI)

db = client['mhrbuilds']