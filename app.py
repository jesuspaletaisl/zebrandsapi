import falcon.asgi
import logging

from db import DB
from model import Model


from api.session import Session
from api.user import User
from api.product import Product
from api.docs import Docs

from mw import AuthMiddleware

logging.basicConfig(
    level=2,
    format="%(asctime)-15s %(levelname)-8s %(message)s"
)

def create_app(config=None):
    authm = AuthMiddleware()

    app = falcon.asgi.App(middleware=[])

    env_stage = None
    db = DB(env_stage) #MongoDB
    model = Model()

    session = Session(db, model)    
    user = User(db, model)
    product = Product(db, model)
    docs = Docs()

    app.add_route('/token', session, suffix='token')


    app.add_route('/users', user, suffix='users')
    app.add_route('/users/{user_id}', user, suffix='user')
    app.add_route('/users/{user_id}/transactions', user, suffix='transactions')

    app.add_route('/products', product, suffix='products')
    app.add_route('/products/{product_id}', product, suffix='product')

    app.add_route('/docs', docs, suffix='docs')
    app.add_route('/template', docs, suffix='template')


    return app

app = create_app()
