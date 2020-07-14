from .hello import Hello
from .simple_api import SimpleApi
from .packages_api import PackagesApi


API_ROUTES = [
    (r'/api/hello', Hello),
    (r'/pypi/simple/([\w\.\d\-\_]+)/', SimpleApi),
    (r'/pypi/packages/(.*)', PackagesApi),
]