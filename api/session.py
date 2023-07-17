import falcon

class Session:
    def __init__(self, db, model):
        self.__db = db

        self.model = model

    async def on_post_token(self, req, resp):
        body = await req.media

        validation = self.model.validate("session", body)

        if "error" in validation:
            resp.media = {
                "error": validation["error"]
            }
            resp.status = falcon.HTTP_400
            return None

        try:
            token = self.__db.encode_jwt(body)
        except Exception as ex:
            resp.media = {
                "error": str(ex)
            }
            resp.status = falcon.HTTP_400
            return None

        resp.media = {"token": token}

        resp.status = falcon.HTTP_200
