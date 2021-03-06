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

def add_user(userid):
    user_ref = db.collection(u'users').document(str(userid))
    user_ref.set({
        u'id': userid,
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

def add_payment(userid,amount,eventid,payload,title):
    payment_ref = db.collection(u'payment').document(payload)
    payer=fetch_profile(userid)
    payment_ref.set({
        u'id':userid,
        #u'request_from': request_from,
        u'amount': amount,
        u'eventid': eventid,
        u'completed':False,
        u'payload':payload,
        u'event_name': title,
        u'payer_name':payer['name'],
        u'date': datetime.datetime.now(),
    })


# after the payee click the link, the request_from will be update to this payment
def complete_payment(payload,request_from):
    payment_ref = db.collection(u'payment').document(payload)
    payee=fetch_profile(request_from)
    payment_ref.update({
        u'request_from': request_from,
        u'payee_name':payee['name'],
    })

def finish_payment(payload):
    payment_ref = db.collection(u'payment').document(payload)
    payment_ref.update({
        u'completed': True,
    })

def fetch_payment_by_id(payload):
    payment_ref = db.collection(u'payment').document(payload)
    doc = payment_ref.get()
    if doc.exists:
        logger.info(f'Document data: {doc.to_dict()}')
        return doc.to_dict()
    else:
        logger.info(u'No such document!')





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

def fetch_ongoing_payment(userid):
    result=[]
    docs = db.collection(u'payment').where(u'id', u'==', userid).where(u'completed', u'==', False).stream()
    if not docs:
        logger.info(u'No such document!')
    else:
        for doc in docs:
            #logger.info(f'Document data: {doc.to_dict()}')     
            result.append(doc.to_dict())
    return result

def fetch_all_unpaid(userid):
    result=[]
    docs = db.collection(u'payment').where(u'request_from', u'==', userid).where(u'completed', u'==', False).stream()
    if not docs:
        logger.info(u'No such document!')
    else:
        for doc in docs:
            #logger.info(f'Document data: {doc.to_dict()}')  
            result.append(doc.to_dict())     
    return result

def fetch_all_unfinished_events(userid):
    result=[]
    docs = db.collection(u'event').where(u'userid', u'==', userid).stream()
    if not docs:
        logger.info(u'No such document!')
    else:
        for doc in docs:
            data = doc.to_dict()
            print(data)
            data['eventid']=doc.id
            if(not check_complete(data['userid'],doc.id)):
                print(data['eventid'])
                result.append(data)
    return result

def check_complete(userid,eventid):
    docs = db.collection(u'payment').where(u'id', u'==', userid).where(u'eventid',u'==',eventid).stream()
    if not docs:
        logger.info(u'No such document!')
    else:
        for doc in docs:
            if(not doc.to_dict()['completed']):
                return False
    return True   
            
def fetch_payments_of_event(eventid):
    result=[]
    docs = db.collection(u'payment').where(u'eventid', u'==', eventid).stream()
    if not docs:
        logger.info(u'No such document!')
    else:
        for doc in docs:
            result.append(doc.to_dict())     
    return result

def add_event(userid,title):
    eventid=str(uuid.uuid1())
    event_ref = db.collection(u'event').document(eventid)
    event_ref.set({
        u'userid':userid,
        u'date': datetime.datetime.now(),
        u'title': title,
    })

    return eventid

def fetch_event(eventid):
    event_ref = db.collection(u'event').document(eventid)
    doc = event_ref.get()
    if doc.exists:
        logger.info(f'Document data: {doc.to_dict()}')
        return doc.to_dict()
    else:
        logger.info(u'No such document!')


def update_event_status(doc_id):
    event_ref = db.collection(u'event').document(doc_id)

    event_ref.update({
        u'completed':True,
    })

def change_notification(eventid,bool):
    event_ref = db.collection(u'event').document(str(eventid))
    event_ref.update({
        u'notification':bool,
    })

def change_notification_frequency(eventid,fre):
    event_ref = db.collection(u'event').document(str(eventid))
    event_ref.update({
        u'frequency':fre,
    })




       


