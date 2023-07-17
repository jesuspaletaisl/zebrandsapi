import falcon

class Session:
    def __init__(self, db, model):
        self.__db = db

        self.model = model

    async def on_post_token(self, req, resp):
        body = await req.media

        token = self.__db.encode_jwt(body)

        resp.media = {"token": token}

        resp.status = falcon.HTTP_200
