import falcon
import asyncio
from functools import partial

class Product:
    def __init__(self, db, model):
        self.__db = db

        self.model = model

    async def set_emails(self, product_id):
        #Send email to admin users
        admins = await self.__db.list_docs("users", {"role": "admin"}, {"email": 1})

        async for admin in admins:
            data = {
            'Messages': [
                {
                "From": {
                    "Email": "support@paperchain.space",
                },
                "To": [
                    {
                    "Email": admin["email"]
                    }
                ],
                "Subject": "Greetings from Zebrands API.",
                "TextPart": "Zebrands API changes",
                "HTMLPart": "<h3>Dear admin user,</h3><br />The product with ID {} has been modified.".format(product_id),
                "CustomID": "ProductChanged"
                }
            ]
            }
            res = self.__db.send_email(data)
            await asyncio.sleep(1)


    async def on_get_product(self, req, resp, product_id): #get_product
        product = await self.__db.get_doc('products', {"id": product_id})

        #Update number of times product is queried by anonymous user
        token = req.headers.get("authorization", " ").split(" ")[-1]
        creds = await self.__db.validate_token(token)
        
        if creds.get("role", "") != "admin":
            
            query = {"user_id": creds["id"], "product_id": product_id}
            is_trx = await self.__db.get_doc("transactions", query, {"id": 1})

            if not is_trx:
                query["counter_view"] = 1
                query["id"] = self.__db.create_id()
                query["created_at"] = self.__db.create_date()
                await self.__db.insert_doc("transactions", query)
            else:
                cond = {"$inc": {"counter_views": 1}}
                await self.__db.update_doc("transactions", query, cond = cond)

        resp.media = product
        resp.status = falcon.HTTP_200

    async def on_post_products(self, req, resp): #create_product
        body = await req.media

        #Verify fields in body
        validation = self.model.validate("product", body)

        if "error" in validation:
            resp.media = {
                "error": validation["error"]
            }
            resp.status = falcon.HTTP_400
            return None

        #Verify if user is admin
        token = req.headers.get("authorization", " ").split(" ")[-1]
        creds = await self.__db.validate_token(token)
        if creds.get("role", "") != "admin":
            resp.media = {
                "error": "User does not have admin privileges"
            }
            resp.status = falcon.HTTP_400
            return None

        #Create new product in db
        body["id"] = self.__db.create_id()
        body["created_at"] = self.__db.create_date()

        product_id = await self.__db.insert_doc("products", body)

        if not product_id:
            resp.media = {"error": "Product not created"}
            resp.status = falcon.HTTP_400
            return None

        resp.media = {"id": product_id}

        resp.status = falcon.HTTP_200

    async def on_patch_product(self, req, resp, product_id): #update_product
        body = await req.media

        validation = self.model.validate("product", body)

        if "error" in validation:
            resp.media = {
                "error": validation["error"]
            }
            resp.status = falcon.HTTP_400
            return None

        #Verify if user is admin
        token = req.headers.get("authorization", " ").split(" ")[-1]
        creds = await self.__db.validate_token(token)
        if creds.get("role", "") != "admin":
            resp.media = {
                "error": "User does not have admin privileges"
            }
            resp.status = falcon.HTTP_400
            return None

        cond = {"$set": body}

        res = await self.__db.update_doc('products', {"id": product_id}, cond)

        if not res:
            resp.media = {"error": "Product not updated"}
            resp.status = falcon.HTTP_400
            return None

        resp.status = falcon.HTTP_204

        funcp = partial(self.set_emails, product_id)

        resp.schedule(funcp)

    async def on_delete_product(self, req, resp, product_id): #delete_product
        #Verify if user is admin
        token = req.headers.get("authorization", " ").split(" ")[-1]
        creds = await self.__db.validate_token(token)
        if creds.get("role", "") != "admin":
            resp.media = {
                "error": "User does not have admin privileges"
            }
            resp.status = falcon.HTTP_400
            return None


        res = await self.__db.delete_doc('products', {"id": product_id})

        if not res:
            resp.media = {"error": "Product not deleted"}
            resp.status = falcon.HTTP_400
            return None

        resp.status = falcon.HTTP_200

    