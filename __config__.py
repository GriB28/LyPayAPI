from os import getcwd


class CONFIGURATION:
    CACHEPATH = getcwd() + '/lypay_api_cache/'

    CHUNK_SIZE = 512

    JWT_KEY = "crimsonmoonshinesuponatownthatissmearedinblood-criedthedivagivenintolament"

    HOST = "http://localhost"
    PORT = 8128


VERSION = "v2.4.2a"
NAME = "API Release"
BUILD = 13
