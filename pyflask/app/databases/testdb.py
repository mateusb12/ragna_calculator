import db_operations as dbo

random_u = dbo.random_user()
dbo.create_user(random_u.username, random_u.password, random_u.email)