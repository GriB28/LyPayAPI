from ssl import create_default_context as ssl_create_default_context, CERT_NONE
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class CONFIGURATION:
    CACHEPATH = 'media'

    CHUNK_SIZE = 512

    JWT_KEY = "crimsonmoonshinesuponatownthatissmearedinblood-criedthedivagivenintolament"

    HOST = getenv("LYPAY_HOST")
    PORT = int(getenv("LYPAY_PORT"))

    SSL = ssl_create_default_context()
    SSL.check_hostname = False
    SSL.verify_mode = CERT_NONE


VERSION = "v2.5a"
NAME = "API Update 1"
BUILD = 18
