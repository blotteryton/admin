import json

import requests
from django.conf import settings
from django.core.cache import cache


def convert_ton_rub(balance):
    if not balance:
        return 0

    rate = cache.get("ton_rub")
    if not rate:
        rate = requests.get(f"{settings.RATES_SERVICE_URL}/rates/toncoin/RUB").json().get("rate")
        cache.set("ton_rub", rate, 300)

    return round(balance * rate, 2)


def convert_ton_usd(balance):
    if not balance:
        return 0

    rate = cache.get("ton_usd")
    if not rate:
        rate = requests.get(f"{settings.RATES_SERVICE_URL}/rates/toncoin/USD").json().get("rate")
        cache.set("ton_usd", rate, 300)

    return round(balance * rate, 2)


def create_transfer(source_wallet, mnemonic: str, dest_wallet, amount, comment=""):
    data = {
          "sourceWallet": source_wallet,
          "mnemonic": json.loads(mnemonic.replace("'", "\"")),
          "destWallet": dest_wallet,
          "amount": float(amount),
          "comment": comment
        }

    return requests.post(f"{settings.TONEX_DOMAIN}/api/v1/wallets/transfer", json=data)
