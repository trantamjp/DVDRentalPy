from app.models.country import *
from app.models.city import *
from app.models.address import *
from app.models.customer import *
from app.models.language import *
from app.models.category import *
from app.models.actor import *
from app.models.film import *


class ModelFactory():
    country = Country
    city = City
    address = Address
    customer = Customer
    language = Language
    category = Category
    actor = Actor
    film = Film
