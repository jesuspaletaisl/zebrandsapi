import falcon

class User:
    def __init__(self, db, model):
        self.__db = db

        self.model = model

    async def on_get_user(self, req, resp, user_id): #get_user
        user = await self.__db.get_doc('users', {"id": user_id})
        resp.media = user

        resp.status = falcon.HTTP_200

    async def on_get_transactions(self, req, resp, user_id): #list_transactions
        trxs = await self.__db.list_docs('transactions', {"user_id": user_id})
        resp.media = {"transactions": [trx async for trx in trxs]}

        resp.status = falcon.HTTP_200

    async def on_post_users(self, req, resp): #create_user
        body = await req.media

        validation = self.model.validate("user", body)

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

        body["id"] = self.__db.create_id()
        body["created_at"] = self.__db.create_date()

        user_id = await self.__db.insert_doc('users', body)

        if not user_id:
            resp.media = {"error": "User not created"}
            resp.status = falcon.HTTP_400
            return None

        resp.media = {"id": user_id}

        resp.status = falcon.HTTP_201

    async def on_patch_user(self, req, resp, user_id): #update_user
        body = await req.media

        #Verify fields in body
        validation = self.model.validate("user", body)

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

        res = await self.__db.update_doc('users', {"id": user_id}, cond)

        if not res:
            resp.media = {"error": "User not updated"}
            resp.status = falcon.HTTP_400
            return None

        resp.status = falcon.HTTP_204

    async def on_delete_user(self, req, resp, user_id): #delete_user
        #Verify if user is admin
        token = req.headers.get("authorization", " ").split(" ")[-1]
        creds = await self.__db.validate_token(token)
        if creds.get("role", "") != "admin":
            resp.media = {
                "error": "User does not have admin privileges"
            }
            resp.status = falcon.HTTP_400
            return None


        res = await self.__db.delete_doc('users', {"id": user_id})

        if not res:
            resp.media = {"error": "User not deleted"}
            resp.status = falcon.HTTP_400
            return None

        resp.status = falcon.HTTP_200