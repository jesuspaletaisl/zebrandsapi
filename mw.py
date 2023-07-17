import falcon

class AuthMiddleware:
    def __init__(self):
        pass

    async def process_startup(self, scope, event):
        pass

    async def process_request(self, req, resp):
        token = req.get_header('Authorization')

        #print("sub", req.relative_uri)

        if not token and req.relative_uri != "/token":
            resp.media = {"error": "Authorization header not found"}
            resp.status = falcon.HTTP_400
            resp.complete = True
            return None

    