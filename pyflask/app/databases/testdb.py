import db_operations as dbo
from app.models.tables import User

# random_u = dbo.random_user()
# dbo.create_user(random_u.username, random_u.password, random_u.email)

# dbo.UserQuery.user_insert_new_param([500, 503, 504], 'premium', 'True')
# dbo.UserQuery.user_insert_new_param([501, 502, 505, 506, 507], 'premium', 'False')

# dbo.UserDB.delete_old_param([], 'premium')

# dbo.UserDB.insert_new_param([], 'premium', 'False')


# user1 = User("admin45", "123456", "Admin", "admin@hotmail.com")
# print(user1)

# print(dbo.UserDB.login("charlesthompson", "afbdmx28m"))

print(dbo.UserDB.get_by_id('500'))