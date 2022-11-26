"""
Description: Using python 2
1. Creates a product type
2. Creates a product using that product type if it does not already exist
3. Creates an engagement within that product
4. Uploads 2 vulnerability scan results
"""
from random import randint
from datetime import datetime, timedelta
import os
import requests
import json
import time


# *************************SETUP CONNECTION SECTION***************************
host = 'http://20.55.28.161:8080/'
api_key = cc8481d743fd4818629af6d6f2cfcd4ef7a80b2a
key = 'Token ' + api_key
user_id = 2 #default user
prod_name = "Javulna" #Product Name
prod_desc = "A very detailed description"
eng_name = "Javulna_Engagement" #Engagement Name
start_date = datetime.now()
end_date = start_date+timedelta(days=180)
zap_path = '/home/defectdojo/Security-test/ZAP-01-Result.xml' #path to scan result
Upload_headers = {
    'Authorization': key,
}
headers = {
    'Authorization': key,
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

# *************************PRODUCT TYPE SECTION***************************
#Create product type function:
def create_prod_type():
    data = {
        "name": "Research And Production", 
        "created": start_date.strftime("%Y-%m-%d"), 
        "updated": start_date.strftime("%Y-%m-%d"), 
        "critical_product": False, 
        "key_product": False
        }
    response = requests.post(host+'/api/v2/product_types/', headers=headers, data=json.dumps(data))
    print "Creating Product Type response: " + str(response)
create_prod_type()

# *************************PRODUCT SECTION***************************

def get_product_id(p_name):
    products = requests.get(host+'/api/v2/products/', headers=headers)
    data = json.loads(products.text)
    for product in data["results"]:
        if p_name == product['name']:
            product_id = product['id']
            return product_id

prod_id = get_product_id(prod_name)

def create_product(p_name):
    data = {
        "name": p_name,
        "description": prod_desc,
        "prod_type": 1,
    }
    if prod_id == None:
        response = requests.post(host+'/api/v2/products/', headers=headers, data=json.dumps(data))
        print "[+] Product creation response: " + str(response)
    else:
        print "[-] Product not created as it already exists ID: " + str(prod_id)

create_product(prod_name)

# *************************ENGAGEMENT SECTION***************************

def get_engagement_id(e_name):
    engagements = requests.get(host+'/api/v2/engagements/', headers=headers)
    data = json.loads(engagements.text)
    for engagement in data["results"]:
        if e_name == engagement['name'] and engagement['product'] == prod_id:
            e_id = engagement['id']
            return e_id

eng_id = get_engagement_id(eng_name)

def create_engagement(e_name):
    data = {
        "status": "In Progress", 
        "product": prod_id, 
        "name": e_name, 
        "lead": user_id, 
        "target_end": end_date.strftime("%Y-%m-%d"), 
        "target_start": start_date.strftime("%Y-%m-%d")
    }
    if eng_id == None:
        response = requests.post(host+'/api/v2/engagements/', headers=headers, data=json.dumps(data))
        print "[+] Engagement creation response: " + str(response)
    else:
        print "[-] Engagement not created as it already exists ID: " + str(eng_id)

prod_id = get_product_id(prod_name)
create_engagement(eng_name)

# *************************UPLOAD RESULTS SECTION***************************

def upload(path, scanType):
    # Assignment: Finish the upload function
    eng_id = get_engagement_id(eng_name)
    upload(zap_path, 'ZAP Scan')
    files = {
        'file': ('ZAP-01-Result.xml', open('/home/defectdojo/Security-test/ZAP-01-Result.xml','rb')),
        'scan_type': (None, 'ZAP Scan'),
        'tags': (None, 'api'),
        'verified': (None, 'false'),
        'active': (None, 'true'),
        'scan_date': (None, start_date.strftime("%Y-%m-%d")),
        'engagement': (None, eng_id),
    }
    response = requests.post(host+'/api/v2/import-scan/', headers=Upload_headers, files=files)
    print "[+] Uploading " + 'ZAP Scan' +" Response: "+ str(response)

    
