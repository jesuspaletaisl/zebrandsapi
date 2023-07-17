import argparse, json
import httpx

import asyncio

class TestApi:
    def __init__(self, env):
        self.urls = {
            "local": "http://127.0.0.1:8000",
            "dev": "https://zebrandsapi-develop.up.railway.app"
        }

        self.url = self.urls[env]

        self.loop = asyncio.new_event_loop()

        self.ss = httpx.AsyncClient()

        self.super_admin = {
            "client_id": "admin",
            "client_secret": "pass"
        }

    def get_headers(self, headers):
        return {"Authorization": "Bearer {}".format(headers["token"])}

    def get_url(self, subd):

        url = [self.url]
        url.extend(subd)

        return "/".join(url)

    def run(self, func_loop):
        return self.loop.run_until_complete(func_loop)

    async def test_token(self, body):
        url = self.get_url(["token"])

        res = await self.ss.post(url, json = body)
        token = res.json()

        #print("Token", json.dumps(token, indent=4))

        return token

    async def test_user_admin(self):
        #Get auth token
        token = await self.test_token(self.super_admin)

        print("Super Token", json.dumps(token, indent=4))
        headers = self.get_headers(token)

        #New user admin
        url = self.get_url(["users"])

        body = {"role": "admin", "email": "support@paperchain.space", "secret_key": "pass"}

        res = await self.ss.post(url, json = body, headers = headers)
        user_admin = res.json()

        print("New user admin", json.dumps(user_admin, indent=4))

        user_admin["secret_key"] = "pass"

        return user_admin

    async def test_user_anon(self):
        #Get auth token
        token = await self.test_token(self.super_admin)

        print("Super Token", json.dumps(token, indent=4))
        headers = self.get_headers(token)

        #New user admin
        url = self.get_url(["users"])

        body = {"role": "anonymous", "email": "support@paperchain.space", "secret_key": "pass"}

        res = await self.ss.post(url, json = body, headers = headers)
        user = res.json()

        print("New user anon", json.dumps(user, indent=4))

        user["secret_key"] = "pass"

        return user

    async def test_user(self):
        #Get auth token
        token = await self.test_token(self.super_admin)

        print("Super Token", json.dumps(token, indent=4))
        headers = self.get_headers(token)

        #New User
        url = self.get_url(["users"])

        body = {"role": "anonymous", "email": "test@example.com", "secret_key": "pass"}

        res = await self.ss.post(url, json = body, headers = headers)
        user = res.json()

        print("New user", json.dumps(user, indent=4))


        url = self.get_url(["users", user["id"]])
        
        #Update User

        body = {"role": "anonymous", "email": "zebrandstemp@skiff.com", "secret_key": "pass2"}

        res = await self.ss.patch(url, json = body, headers = headers)

        print("User changed", res)

        res = await self.ss.get(url, headers = headers)
        user = res.json()

        print("Get user", json.dumps(user, indent=4))


        #Delete User
        res = await self.ss.delete(url, headers = headers)
        print("User deleted", res)


    async def test_product(self):
        #New user
        user = await self.test_user_admin()

        #Get auth token
        token = await self.test_token({"client_id": user["id"], "client_secret": "pass"})

        print("Token", json.dumps(token, indent=4))
        headers = self.get_headers(token)

        #New Product
        url = self.get_url(["products"])

        body = {
            "sku": "AN3013", 
            "name": "Almohadas Nooz Responsive Foam-REG", 
            "price": 3398, 
            "brand": "NOOZ"
        }

        res = await self.ss.post(url, json = body, headers = headers)
        product = res.json()

        print("New Product", json.dumps(product, indent=4))

        url = self.get_url(["products", product["id"]])
        
        #Update User

        body = {
            "sku": "AN3014", 
            "name": "Almohadas Nooz Responsive Foam-REG", 
            "price": 2198, 
            "brand": "NOOZ"
        }

        res = await self.ss.patch(url, json = body, headers = headers)

        print("Product changed", res)


        #New user Anon
        user = await self.test_user_anon()

        #Get auth token
        token = await self.test_token({"client_id": user["id"], "client_secret": "pass"})

        print("Token", json.dumps(token, indent=4))
        headers_a = self.get_headers(token)

        res = await self.ss.get(url, headers = headers_a)
        product = res.json()

        print("Get product", json.dumps(product, indent=4))

        uri_logs = self.get_url(["users", user["id"], "transactions"])

        res = await self.ss.get(uri_logs, headers = headers_a)
        trxs = res.json()

        print("List transactions", json.dumps(trxs, indent=4))

        #Delete Product
        res = await self.ss.delete(url, headers = headers)
        print("Product deleted", res)


    def test(self, case_test):
        opts = {
            "user": self.test_user,
            "product": self.test_product
        }

        return self.run(opts.get(case_test, "user")())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='API testing')
    parser.add_argument('--env', type=str, required=False)
    parser.add_argument('--opt', type=str, required=True)

    
    args = parser.parse_args()

    testch = TestApi(args.env)

    testch.test(args.opt)