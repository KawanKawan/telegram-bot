from typing import Dict

ID="123"
name="JJ"
phone="12345678"
paymentmethod="PayNow"

profile = {
        "ID":ID,
        "Name": name,
        "Phone": phone,
        "Payment Method": paymentmethod
    }

def fetch_profile(userID):
    return profile

def update_profile(newprofile):
    profile.update(newprofile)

       


