from ssl import create_default_context as ssl_create_default_context, CERT_NONE
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / '.env')

class CONFIGURATION:
    CACHEPATH = 'media'

    CHUNK_SIZE = 8192

    JWT_KEY = "crimsonmoonshinesuponatownthatissmearedinblood-criedthedivagivenintolament"

    HOST = getenv("LYPAY_CORE_HOST")
    PORT = int(getenv("LYPAY_CORE_PORT"))
    TOKEN = getenv("LYPAY_CORE_TOKEN") if getenv("LYPAY_CORE_TOKEN") != '' else None

    SSL = ssl_create_default_context()
    SSL.check_hostname = False
    SSL.verify_mode = CERT_NONE


VERSION = "v3.1a"
NAME = "Release 3: global fixes"
BUILD = 24
