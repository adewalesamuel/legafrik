from os import environ
import stripe


from environs import Env

env = Env()
env.read_env()

class Stripe:
    __SECRET = environ["STRIPE_SECRET"]

    def __init__(self) -> None:
        pass

    def make_payment(self, request_data):
        stripe.api_key = self.__SECRET
        
        try:
            stripe.Charge.create(stripe.api_key, 
                amount=request_data['amount'],
                currency=request_data['currency'],
                source=request_data['source'],
                description=request_data['description'])
        except Exception as err:
            raise Exception(err)