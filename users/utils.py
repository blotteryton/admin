import requests
from django.conf import settings
from django.core.cache import cache
from django.db import connections


def table_exists(table_name: str, connection_name: str = "default") -> bool:
    return table_name in connections[connection_name].introspection.table_names()


def create_wallet(user, domain: str = settings.TONEX_DOMAIN):
    try:
        if not user.has_wallet:
            response = requests.post(f"{domain}/api/v1/wallets").json()

            user.wallet_address = response.get("address")
            user.wallet_public_key = response.get("publicKey")
            user.wallet_secret_key = response.get("secretKey")
            user.wallet_mnemonic = str(response.get("mnemonic"))
            user.save()
    except Exception as e:
        print(e)


def get_wallet_balance(address: str, domain: str = settings.TONEX_DOMAIN):
    try:
        balance = cache.get(address)
        if balance is not None:
            return balance

        balance = requests.get(f"{domain}/api/v1/wallets/balance", params={"address": address}).json().get("balance")

        cache.set(address, balance, 30)
        return balance
    except Exception as e:
        print(e)
