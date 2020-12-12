from app.models.tables import FireUser
from random import choice

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
if db_list:
    db_amount = len(db_list.values())
else:
    db_amount = 0


def create_user(username: str, password: str, email: str):
    if not existing_check(username, email):
        id_base = 500
        creation_id = generate_id() + id_base
        aux = {"id": creation_id,
               "username": username,
               "password": password,
               "email": email}

        db.child("users").child(creation_id).set(aux)
        return True
    else:
        return existing_reason(username, email)


def read_user(input_id: int):
    return db.child("users").child(input_id).get().val()


def update_user(input_id: int, params: FireUser):
    ref = db.child("users").child(input_id)
    aux = {"id": params.id,
           "username": params.username,
           "password": params.password,
           "email:": params.email}
    ref.set(aux)


def delete_user(input_id: int):
    db.child("users").child(input_id).remove()


def existing_check(username: str, email: str):
    if db_list:
        for i in db_list.values():
            if username == i['username'] or email == i['email']:
                return True
        return False
    return None


def existing_reason(username: str, email: str):
    reasons = []
    if db_list:
        for i in db_list.values():
            if username == i['username']:
                reasons.append("username")
            if email == i['email']:
                reasons.append("email")
    return reasons


def generate_id():
    if db_list:
        list_size = len(db_list.values())
    else:
        list_size = 0
    return list_size


def random_user():
    user_list = ("harveyshelton", "billsanders", "christinedavidson",
                 "charlesthompson", "maryrussell", "bradleyjames",
                 "gabriellacurtis", "kenziaustin", "nicolearnold"
                 "tomgonzales", "bobhorton", "derekmason")
    email_list = ("harvey.shelton@gmail.com", "bill.sanders@example.com", "christine.davidson@example.com",
                  "charles.thompson@example.com", "mary.russell@example.com", "bradley.james@example.com",
                  "gabriella.curtis@example.com", "kenzi.austin@example.com", "nicole.arnold@example.com",
                  "tom.gonzales@example.com", "bob.horton@example.com", "derek.mason@example.com")
    password_list = ("tcxyyw465", "3zka8xhy8", "kt5b8y4g7",
                     "afbdmx28m", "chcfxa7gt", "8rxecz5gm",
                     "88nzxfp3z", "zmdeb597z", "w9ahe6j33",
                     "422erbfcv", "dcjb72v6n", "xpvtk6t65")
    final_list = list(zip(user_list, password_list, email_list))
    random_choice = choice(final_list)
    return FireUser(1, random_choice[0], random_choice[1], random_choice[2])