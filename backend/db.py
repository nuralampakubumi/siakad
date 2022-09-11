
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCmbuHotAazJQBuADMYx_kZssGa-KI1W_s",
    "authDomain": "siakad-6280f.firebaseapp.com",
    "databaseURL": "https://siakad-6280f-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "siakad-6280f",
    "storageBucket": "siakad-6280f.appspot.com",
    "messagingSenderId": "267728407389",
    "appId": "1:267728407389:web:a18641a836adfb77d9f6b4"
}


firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)


db = firestore.client()

def get_all_collection(collection, orderBy=None, direction=None):
    if orderBy:
        collects_ref = db.collection(collection).order_by(
            orderBy, direction=direction)
    else:
        collects_ref = db.collection(collection)
    collects = collects_ref.stream()
    RETURN = []
    for collect in collects:
        ret = collect.to_dict()
        ret['id'] = collect.id
        RETURN.append(ret)
    return RETURN


# ===================================================================
