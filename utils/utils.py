import random
import string
from django.conf import settings

from storages.backends.azure_storage import AzureStorage


def get_code():
    return random.randint(1000, 9999)


def generate_random_token():
    # Generate a random 6-digit token
    return ''.join(random.choices(string.digits, k=6))


class AzureMediaStorage(AzureStorage):
    azure_account_name = settings.AZURE_BLOB_STORAGE_ACCOUNT
    azure_account_key = settings.AZURE_BLOB_KEY
    azure_container = settings.AZURE_BLOB_CONTAINER_NAME
    expiration_secs = None
