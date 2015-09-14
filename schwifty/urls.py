from schwifty.endpoints import *
from schwifty.core import api

urls = [
    (Welcome, "/"),
    (Search, "/search/"),
    (Detail, "/detail/<str:datatype>/<int:eid>/"),
]

for url in urls:
    api.add_resource(*url)
