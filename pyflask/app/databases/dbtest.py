from db_config import get_all_users
from app.models.tables import FireUser

lista = get_all_users()

user2 = {'email:': 'rauna@hotmail.com', 'id': 1562, 'name': 'Rauna', 'password': '123456', 'username': 'raunab12'}


for key, value in lista.items():
    print(key, value)

print("é ou não é? {}".format(user2 in lista.values()))
