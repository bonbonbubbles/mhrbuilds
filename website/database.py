from pymongo import MongoClient
import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.environ['MONGODB_URI']

client = MongoClient(MONGODB_URI)

db = client['mhrbuilds']