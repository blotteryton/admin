import json
import requests

from io import BytesIO

from django.conf import settings

from administration.models import Configuration
from requests_toolbelt.multipart.encoder import MultipartEncoder


def upload_file(filename, file, file_format) -> dict:
    fields = MultipartEncoder({
        "file": (filename, file, file_format)
    })

    return requests.post(f"{settings.IPFS_API_DOMAIN}/api/v1/upload", data=fields,
                         headers={"Content-Type": fields.content_type}).json()


def get_collection_content_uri(name, description, image, external_link, seller_fee_basis_points, fee_recipient):
    image_url = upload_file(image._name, image.file, image.content_type).get("url")
    if not image_url:
        return

    content = BytesIO()
    content.write(json.dumps({
        "name": name,
        "description": description,
        "image": image_url,
        "external_link": external_link,
        "seller_fee_basis_points": seller_fee_basis_points,
        "fee_recipient": fee_recipient,
    }).encode())

    return upload_file("collection.json", content, "application/json").get("url")


def get_nft_content_uri(name, description, image, external_link):
    image_url = upload_file(image._name, image.file, image.content_type).get("url")
    if not image_url:
        return

    content = BytesIO()
    content.write(json.dumps({
        "name": name,
        "description": description,
        "image": image_url,
        "external_link": external_link,
    }).encode())

    return upload_file("nft.json", content, "application/json").get("fileHash")


def create_collection(user, name, description, image, categories, configuration=None):
    try:
        if configuration is None:
            configuration = Configuration.get_solo()

        fee_recipient = configuration.collection_create_fee_recipient
        if fee_recipient == "self":
            fee_recipient = user.wallet_address

        collection_content_uri = get_collection_content_uri(
            name=name,
            description=description,
            image=image,
            external_link=configuration.collection_create_external_link,
            seller_fee_basis_points=configuration.collection_create_seller_fee_basis_points,
            fee_recipient=fee_recipient
        )

        if not collection_content_uri:
            return

        data = {
            "mnemonic": json.loads(user.wallet_mnemonic.replace("'", "\"")),
            "amount": configuration.collection_create_amount,
            "collectionContentUri": {collection_content_uri},
            "nftItemContentBaseUri": configuration.nft_item_content_base_uri,
            "royalty": configuration.collection_create_royalty,
            "royaltyAddress": configuration.collection_create_royalty_address
        }

        return requests.post(url=f"{settings.TONEX_DOMAIN}/api/v1/nft/createCollection", data=data).json()
    except Exception as e:
        print(e)


def create_nft(user, collection, name, description, price, image, configuration=None):
    try:
        if configuration is None:
            configuration = Configuration.get_solo()

        nft_content_uri = get_nft_content_uri(
            name=name,
            description=description,
            image=image,
            external_link=configuration.collection_create_external_link,
        )

        if not nft_content_uri:
            return

        data = {
            "collectionAddress": collection.address,
            "amount": float(price),
            "mnemonic": json.loads(user.wallet_mnemonic.replace("'", "\"")),
            "nftItemContentBaseUri": configuration.nft_item_content_base_uri,
            "nftItemContentUri": nft_content_uri,
        }

        return requests.post(url=f"{settings.TONEX_DOMAIN}/api/v1/nft/createNft", data=data).json()
    except Exception as e:
        print(e)
