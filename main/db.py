from typing import Dict
import logging
import datetime
import uuid
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
        u'id': userid,
        u'Name': name,
        u'Phone': phone,
        u'Payment Method': PAYMENT_METHOD[payment_method]
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

    user_ref.update({
        category:text,
    })

def add_payment(userid,request_from,amount,eventid,payload):
    payment_ref = db.collection(u'payment').document(str(uuid.uuid1()))
    payment_ref.set({
        u'id':userid,
        u'request_from': request_from,
        u'amount': amount,
        u'eventid': eventid,
        u'completed':False,
        u'payload':payload
    })

def update_payment_amount(userid,request_from,eventid,amount):
    payment_ref = db.collection(u'payment')
    docs = db.collection(u'payment').where(u'id', u'==', userid).where(u'request_from',u'==',request_from).where(u'eventid',u'==',eventid).get()
    if not docs:
        logger.info(u'No such document!')
    else:
        for doc in docs:
            logger.info(f'Document data: {doc.to_dict()}')       
            payment_ref.document(doc.id).update({u'amount':amount})
                            

def update_payment_status(userid,request_from,eventid,completed):
    payment_ref = db.collection(u'payment')
    docs = db.collection(u'payment').where(u'id', u'==', userid).where(u'request_from',u'==',request_from).where(u'eventid',u'==',eventid).get()
    # print(len(list(docs)))
    if not docs:
        logger.info(u'No such document!')
    else:
        for doc in docs:
            logger.info(f'Document data: {doc.to_dict()}')       
            payment_ref.document(doc.id).update({u'completed':completed})            
            
                                                                     
    
def fetch_payment(userid,request_from,eventid):
    docs = db.collection(u'payment').where(u'id', u'==', userid).where(u'request_from',u'==',request_from).where(u'eventid',u'==',eventid).stream()
    if not docs:
        logger.info(u'No such document!')
    else:
        for doc in docs:
            logger.info(f'Document data: {doc.to_dict()}')       
            return doc.to_dict()

def add_event(userid,title,completed):
    event_ref = db.collection(u'event').document(str(uuid.uuid1()))
    event_ref.set({
        u'userid':userid,
        u'startdate': datetime.date(datetime.now()),
        u'title': title,
        u'completed':completed,
    })

def update_event_status(doc_id):
    event_ref = db.collection(u'event').document(doc_id)

    event_ref.update({
        u'completed':True,
    })

       


