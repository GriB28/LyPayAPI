from os import mkdir
from os.path import exists, join

from .__config__ import CONFIGURATION, VERSION, NAME, BUILD
from . import __exceptions__ as exceptions

from . import user
from . import store
from . import admin
from . import auction
from . import utils
from . import fps

# from . import mst


for path in (
    CONFIGURATION.CACHEPATH,
    join(CONFIGURATION.CACHEPATH, "users_media"),
    join(CONFIGURATION.CACHEPATH, "users_qr"),
    join(CONFIGURATION.CACHEPATH, "stores_media")
):
    if not exists(path):
        mkdir(path)
