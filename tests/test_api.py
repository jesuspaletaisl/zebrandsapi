import argparse, json
import httpx
import pytest
import pytest_asyncio

import asyncio

class TestApi:
    url = "http://127.0.0.1:8000"
    loop = asyncio.new_event_loop()
    ss = httpx.AsyncClient()
    super_admin = {
        "client_id": "admin",
        "client_secret": "pass"
    }
    #url = "https://zebrandsapi-develop.up.railway.app"

    def get_headers(self, headers):
        return {"Authorization": "Bearer {}".format(headers["token"])}

    def get_url(self, subd):

        url = [self.url]
        url.extend(subd)

        return "/".join(url)

    def run(self, func_loop):
        return self.loop.run_until_complete(func_loop)

    @pytest.mark.asyncio
    async def test_token(self):
        body = self.super_admin
        url = self.get_url(["token"])

        res = await self.ss.post(url, json = body)
        token = res.json()

        #print("Token", json.dumps(token, indent=4))

        return token

    @pytest.mark.asyncio
    async def test_user_admin(self):
        #Get auth token
        token = await self.test_token()

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

    @pytest.mark.asyncio
    async def test_user(self):
        #Get auth token
        token = await self.test_token()

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

    @pytest.mark.asyncio
    async def test_product(self):
        #New user
        user = await self.test_user_admin()

        #Get auth token
        self.super_admin = {"client_id": user["id"], "client_secret": "pass"}
        token = await self.test_token()

        print("Token", json.dumps(token, indent=4))
        headers = self.get_headers(token)

        #New Product
        url = self.get_url(["products"])

        body = {"sku": "AN3013", "name": "Almohadas Nooz Responsive Foam-REG", "price": 3398, "brand": "NOOZ"}

        res = await self.ss.post(url, json = body, headers = headers)
        product = res.json()

        print("New Product", json.dumps(product, indent=4))

        url = self.get_url(["products", product["id"]])
        
        #Update User

        body = {"sku": "AN3014", "name": "Almohadas Nooz Responsive Foam-REG", "price": 2198, "brand": "NOOZ"}

        res = await self.ss.patch(url, json = body, headers = headers)

        print("Product changed", res)

        res = await self.ss.get(url, headers = headers)
        product = res.json()

        print("Get product", json.dumps(product, indent=4))


        #Delete User
        res = await self.ss.delete(url, headers = headers)
        print("User deleted", res)