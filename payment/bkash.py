import requests
from django.conf import settings



class BkashService:

    def __init__(self):
        self.base_url = settings.BKASH_BASE_URL
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }


    def grant_token(self):
        url = f"{self.base_url}/tokenized/checkout/token/grant"

        payload = {
            "app_key": settings.BKASH_APP_KEY,
            "app_secret": settings.BKASH_APP_SECRET,
        }

        headers = {
            **self.headers,
            'username': settings.BKASH_USERNAME,
            'password': settings.BKASH_PASSWORD,
        }
    
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        return data.get('id_token')


    def create_payment(self, amount, invoice_number):
        token = self.grant_token()
        url = f"{self.base_url}/tokenized/checkout/create"
        headers = {
            **self.headers,
            'Authorization': token,
            'X-APP-Key': settings.BKASH_APP_KEY,
        }
        payload = {
            "mode": "0011",
            "payerReference": str(invoice_number),
            "callbackURL": "https://altas.duckdns.org/payment/bkash/callback/",
            # "callbackURL": "https://nhlqvk1b-8000.asse.devtunnels.ms/payment/bkash/callback/",
            "amount": str(amount),
            "currency": "BDT",
            "intent": "sale",
            "merchantInvoiceNumber": str(invoice_number),
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()


    def execute_payment(self, payment_id):
        token = self.grant_token()
        url = f"{self.base_url}/tokenized/checkout/execute"
        headers = {
            **self.headers,
            'Authorization': token,
            'X-APP-Key': settings.BKASH_APP_KEY,
        }
        payload = {"paymentID": payment_id}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()