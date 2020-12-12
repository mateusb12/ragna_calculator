from app.models.tables import FireUser

import pyrebase


def start_db():
    config = {
        "apiKey": "AIzaSyDsPdZW45qT8jBQp0EAuGIJe4LDZeKSTBw",
        "authDomain": "ragnacalculator.firebaseapp.com",
        "databaseURL": "https://ragnacalculator-default-rtdb.firebaseio.com",
        "projectId": "ragnacalculator",
        "storageBucket": "ragnacalculator.appspot.com",
        "messagingSenderId": "334339512481",
        "appId": "1:334339512481:web:bc9ca3c8b113e59ea2f8e0",
        "measurementId": "G-WHMMME1PPS"
    }
    firebase = pyrebase.initialize_app(config)
    return firebase.database()


db = start_db()

db_list = db.child("users").get().val()


def push_user(input_id: int, name: str, username: str, password: str, email: str):
    aux = {"id": input_id,
           "name": name,
           "username": username,
           "password": password,
           "email:": email}

    db.child("users").child(input_id).set(aux)


def edit_user(input_id: int, params: FireUser):
    ref = db.child("users").child(input_id)
    aux = {"id": params.id,
           "name": params.name,
           "username": params.username,
           "password": params.password,
           "email:": params.email}
    ref.set(aux)


push_user(1562, "Rauna", "raunab12", "123456", "rauna@hotmail.com")
edit_user(1564, FireUser(1562, "Lincoln", "lincoln15", "123456", "lincoln@hotmail.com"))
