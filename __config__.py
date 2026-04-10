from ssl import create_default_context as ssl_create_default_context, CERT_NONE
from os import getcwd


class CONFIGURATION:
    CACHEPATH = getcwd() + '/lypay_api_cache/'

    CHUNK_SIZE = 512

    JWT_KEY = "crimsonmoonshinesuponatownthatissmearedinblood-criedthedivagivenintolament"

    HOST = "http://localhost"
    PORT = 8128

    SSL = ssl_create_default_context()
    SSL.check_hostname = False
    SSL.verify_mode = CERT_NONE


VERSION = "v2.4.2a"
NAME = "API Release"
BUILD = 13.1
