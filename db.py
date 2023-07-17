import uuid
import pymongo

from datetime import datetime as dt

from motor.motor_asyncio import AsyncIOMotorClient

from mailjet_rest import Client

import base64, jwt

import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

class DB:
    def __init__(self, env = ""):
        uri = MONGO_URI
        self.__client = AsyncIOMotorClient(uri)
        self.__db = self.__client['zebrandsdb']

        self.mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')

    def create_id(self):
        return str(uuid.uuid4())

    def create_date(self):
        return dt.now().strftime("%Y-%m-%d %H:%M:%S")

    def decode_jwt(self, payload):
        key = "secret"
        decoded = jwt.decode(payload, key, algorithms=["HS256"])

        return decoded

    def encode_jwt(self, payload):
        key = "secret"
        encoded = jwt.encode(payload, key, algorithm="HS256")

        return encoded

    async def delete_doc(self, collection, query):
        coll = self.__db[collection]

        try:
            res = await coll.delete_one(query)
            return res.deleted_count
        except Exception as ex:
            print("Exception db: ", ex)
            
            return False


    async def get_doc(self, collection, query, fields = {}):
        coll = self.__db[collection]
        doc = {}

        fields['_id'] = 0

        try:
            doc = await coll.find_one(query, fields)
        except Exception as ex:
            print("Exception db: ", ex)
            
        return doc

    async def insert_doc(self, collection, doc):
        coll = self.__db[collection]

        try:
            result = await coll.insert_one(doc)
            return doc["id"]
        except Exception as ex:
            print("Exception db: ", ex)
            return False

    async def list_docs(self, collection, query, fields = {}):
        coll = self.__db[collection]
        docs = {}

        fields['_id'] = 0

        try:
            docs = coll.find(query, fields)
        except Exception as ex:
            print("Exception db: ", ex)
        return docs

    async def update_doc(self, collection, query, cond):
        coll = self.__db[collection]

        try:
            res = await coll.update_one(query, cond)
            return res.modified_count
        except Exception as ex:
            print("Exception db: ", ex)
            
            return False

    async def validate_token(self, token):
        user_id = self.decode_jwt(token)["id"]


        res = await self.get_doc("users", {"id": user_id}, {"role": 1})

        return True if res["role"] == "admin" else False

    def send_email(self, message):
        result = self.mailjet.send.create(data=message)

        return result



    
