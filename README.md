
# Zebrands API
Catalog System created using Python Falcon Framework, MongoDB and Mailjest service.

Run locally with the next commands:
- Create .env file with variables MONGO_URI, API_KEY and API_SECRET
- pip install pipenv
- pipenv install
- pipenv run uvicorn app:app --reload
- Go to http://127.0.0.1:8000

Dev environment: https://zebrandsapi-develop.up.railway.app/

Documentation: https://zebrandsapi-develop.up.railway.app/docs

For testing purposes in the endpoint /token, the next user was created as admin:

client_id: admin

client_secret: pass

# Architecture design

The Catalog System can be improved adding the next features:
- Connect with an alternative service to Mailjest that allows sending more than 200 emails per day
- Automate the testing process using Github Actions
- Generate different authentication credentials for dev, stg and prod environments.
- Store other types of transactions as logs when users create or delete products.
- Connect the system with a service like Sentry for errors tracking.
