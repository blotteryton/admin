import json

import requests
from django.conf import settings
from django.core.cache import cache

from administration.models import MarketplaceConfiguration, Configuration


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


def deploy_wallet(user, domain: str = settings.TONEX_DOMAIN):
    try:
        if not user.is_wallet_deployed:
            data = {
                "wallet": user.wallet_address,
                "mnemonic": json.loads(user.wallet_mnemonic.replace("'", "\""))
            }

            cache.delete(f"deployed_{user.wallet_address}")
            cache.set(f"send_deploy_{user.wallet_address}", True, 300)
            return requests.post(f"{domain}/api/v1/wallets/deploy", data=data)
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


def get_wallet_deployed(address: str, domain: str = settings.TONEX_DOMAIN):
    try:
        deployed = cache.get(f"deployed_{address}")
        if deployed is not None:
            return deployed

        deployed = True if requests.get(f"{domain}/api/v1/wallets/state",
                                        params={"address": address}).json().get("result") == "active" else False

        cache.set(f"deployed_{address}", deployed, 30)
        return deployed
    except Exception as e:
        print(e)


def create_nft_sale(nft_address, full_price, collection_address, domain: str = settings.TONEX_DOMAIN):
    data = {
        "marketplaceAddress": MarketplaceConfiguration.get_solo().marketplace_address,
        "nftAddress": nft_address,
        "fullPrice": full_price,
        "marketplaceFee": Configuration.get_solo().nft_marketplace_fee,
        "collectionAddress": collection_address,
        "royaltyAmount": Configuration.get_solo().nft_create_royalty
    }

    return requests.post(f"{domain}/api/v1/nft/sale", data=data).json()


def deploy_nft_sale(nft_sale_address, mnemonic: str, domain: str = settings.TONEX_DOMAIN):
    data = {
        "mnemonic": json.loads(mnemonic.replace("'", "\"")),
        "nftSaleAddress": nft_sale_address,
        "marketAddress": MarketplaceConfiguration.get_solo().marketplace_address
    }

    return requests.post(f"{domain}/api/v1/nft/deploySale", data=data)
