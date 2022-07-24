from pymongo import MongoClient
import os
from flask import Flask

MONGODB_URI = "mongodb+srv://bondent89:bh142736@cluster0.asyse.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGODB_URI)

db = client['mhrbuilds']