import msgspec, json

class Session(msgspec.Struct):
    client_id: str
    client_secret: str

class User(msgspec.Struct):
    role: str
    email: str
    secret_key: str

class Product(msgspec.Struct):
    sku: str 
    name: str
    price: int
    brand: str

class Model:
    def __init__(self):
        self.models = {
            "session": Session,
            "user": User,
            "product": Product
        }

    def validate(self, type_id, doc):

        doc = json.dumps(doc)
    
        resp = {}

        try:
            msgspec.json.decode(
                doc,
                type=self.models[type_id]
            )
        except Exception as ex:
            resp = {"error": str(ex)}

        return resp
