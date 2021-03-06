import json
from typing import Tuple, List

import requests

from app.models.tables import FireUser
from random import choice

import pyrebase

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


def start_db():
    firebase_instance = pyrebase.initialize_app(config)
    return firebase_instance.database()


def auth_login(login_str: str, password_str: str):
    firebase_instance = pyrebase.initialize_app(config)
    # create authentication
    auth = firebase_instance.auth()

    # and authenticate the user
    user = auth.sign_in_with_email_and_password(login_str, password_str)
    print("User Created Successfully")
    return user


db = start_db()
# data = {"age": 40, "address": "New York", "employed": True, "name": "John Smith"}
# db.child("people").push(data)
# fu = FireBaseUser()
# auth_db = fu.auth_create_user("gigigogolelel", "phoenix@gmail.com", "123456")
# # auth_db = fu.create("mateusb12", "mateus_b09@hotmail.com", "c139ea31")
# print('oiiiii {}'.format(auth_db))
# my_data = {"name": "Parwiz Forogh"}
# db.child("users").child("OwnKey").set(my_data)

db_list = db.child("users").get().val()
if db_list:
    db_amount = len(db_list.values())
else:
    db_amount = 0

int_id_list = list(db_list.keys())


class User:
    @staticmethod
    def create(username: str, password: str, email: str):
        inner_config = {
            "apiKey": "AIzaSyDsPdZW45qT8jBQp0EAuGIJe4LDZeKSTBw",
            "authDomain": "ragnacalculator.firebaseapp.com",
            "databaseURL": "https://ragnacalculator-default-rtdb.firebaseio.com",
            "projectId": "ragnacalculator",
            "storageBucket": "ragnacalculator.appspot.com",
            "messagingSenderId": "334339512481",
            "appId": "1:334339512481:web:bc9ca3c8b113e59ea2f8e0",
            "measurementId": "G-WHMMME1PPS"
        }
        firebase_instance = pyrebase.initialize_app(inner_config)
        auth = firebase_instance.auth()
        email_flag = None
        username_flag = not UserTools.username_existing_check(username)
        try:
            user = auth.create_user_with_email_and_password(email, password)
            print("User Created Successfully")
            email_flag = True, user
        except requests.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            if error == "EMAIL_EXISTS":
                email_flag = False, "Email already exists"
        if email_flag and username_flag:
            id_base = 500
            creation_id = UserTools.generate_id() + id_base
            aux = {"id": creation_id,
                   "username": username,
                   "password": password,
                   "email": email}

            db.child("users").child(creation_id).set(aux)
            return True
        else:
            return UserTools.existing_reason(username, email)

    @staticmethod
    def create_old(username: str, password: str, email: str):
        if not UserTools.existing_check(username, email):
            id_base = 500
            creation_id = UserTools.generate_id() + id_base
            aux = {"id": creation_id,
                   "username": username,
                   "password": password,
                   "email": email}

            db.child("users").child(creation_id).set(aux)
            return True
        else:
            return UserTools.existing_reason(username, email)

    @staticmethod
    def read(input_id: int):
        return db.child("users").child(input_id).get().val()

    @staticmethod
    def update(input_id: int, params: FireUser):
        ref = db.child("users").child(input_id)
        aux = {"id": params.id,
               "username": params.username,
               "password": params.password,
               "email:": params.email}
        ref.set(aux)

    @staticmethod
    def delete(input_id: int):
        db.child("users").child(input_id).remove()


class UserDB:
    @staticmethod
    def insert_new_param(id_list: list, new_key: str, new_value: str):
        firebase_ids = list(map(int, db_list.keys()))
        if not id_list:
            id_list = firebase_ids
        for i in id_list:
            if i not in firebase_ids:
                raise ValueError("Error: ID [{}] not present in firebase IDs".format(i))
            else:
                aux = db.child("users").child(i).get().val()
                aux[new_key] = new_value
                db.child("users").child(i).set(aux)

    @staticmethod
    def delete_old_param(id_list: list, old_key: str):
        firebase_ids = list(map(int, db_list.keys()))
        if not id_list:
            id_list = firebase_ids
        for i in id_list:
            if i not in firebase_ids:
                raise ValueError("Error: ID [{}] not present in firebase IDs".format(i))
            else:
                aux = db.child("users").child(i).get().val()
                del aux[old_key]
                db.child("users").child(i).set(aux)

    @staticmethod
    def user_query(input_key: str, input_value: str):
        query_list = []
        for i in db_list.values():
            if i[input_key] == input_value:
                query_list.append(i)
        return query_list

    @staticmethod
    def get_by_id(input_id: str):
        for i in db_list.values():
            if i['id'] == int(input_id):
                return i
        return None

    @staticmethod
    def login(input_username: str, input_password: str):
        for i in list(db_list.values()):
            if input_username in i.values() and input_password in i.values():
                return True
        else:
            return False


class UserTools:
    @staticmethod
    def existing_check(username: str, email: str):
        if db_list:
            for i in db_list.values():
                if username == i['username'] or email == i['email']:
                    return True
            return False
        return None

    @staticmethod
    def username_existing_check(username: str):
        if db_list:
            for i in db_list.values():
                if username == i['username']:
                    return True
            return False
        return None

    @staticmethod
    def existing_reason(username: str, email: str):
        reasons = []
        if db_list:
            for i in db_list.values():
                if username == i['username']:
                    reasons.append("username")
                if email == i['email']:
                    reasons.append("email")
        return reasons

    @staticmethod
    def generate_id():
        if db_list:
            list_size = len(db_list.values())
        else:
            list_size = 0
        return list_size

    @staticmethod
    def get_id_list():
        return list(db_list.keys())

    @staticmethod
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
