from typing import Dict

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


def fetch_profile(userID):
    return profile

def update_profile(newprofile):
    profile.update(newprofile)

def add_payment(payment):
    payment.update(payment)
    
def fetch_payment(userID):
    #fetch all payment from db
    return payment

#def update_payment():
       


