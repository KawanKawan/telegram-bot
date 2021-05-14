from typing import Dict
import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

logger = logging.getLogger(__name__)

# Use a service account
cred = credentials.Certificate('firebase-adminsdk.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

PAYMENT_METHOD=["PAYNOW","PAYPAL","PAYLAH","WECHAT"]

def add_user(userid,name,phone,payment_method):
    user_ref = db.collection(u'users').document(str(userid))
    user_ref.set({
        u'name': name,
        u'phone': phone,
        u'payment_method': PAYMENT_METHOD[payment_method]
    })

def fetch_profile(userid):
    doc_ref = db.collection(u'users').document(str(userid))
    doc = doc_ref.get()
    if doc.exists:
        logger.info(f'Document data: {doc.to_dict()}')
        return doc.to_dict()
    else:
        logger.info(u'No such document!')

def update_profile(userid,category,text):
    user_ref = db.collection(u'users').document(str(userid))

    # Set the capital field
    user_ref.update({
        category:text,
    })



userID="0123" #profile id start with 0
name="JJ"
phone="12345678"
paymentmethod="PayNow"

profile = {
        "userID":userID,
        "Name": name,
        "Phone": phone,
        "Payment Method": paymentmethod
    }

userID2="0124" #profile id start with 0
name2="KK"
phone2="12345678"
paymentmethod2="PayNow"

profile2 = {
        "userID":userID2,
        "Name": name2,
        "Phone": phone2,
        "Payment Method": paymentmethod2
    }

ID="1123" #payment id start with 1
userID="0123"
title="movie night"
numOfPeople=5
amount={
    "JJ":10,
    "KongWei":11,
    "Jessica":12,
    "ZiKang":13
}

payment={
    "ID":ID,
    "userID":userID,
    "title":title,
    "numOfPeople":numOfPeople,
    "amount":amount
}



def add_payment(payment):
    payment.update(payment)
    
def fetch_payment(userID):
    #fetch all payment from db
    return payment

#def update_payment():
       


