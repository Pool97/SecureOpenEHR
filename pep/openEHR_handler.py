# This handler is in charge of interfacing the PEP with the openEHR server.
# All the HTTP messages are sent from the PEP according to the openEHR REST API.

import requests, json

openEHR_baseURL = 'http://localhost:8080/ehrbase/rest/openehr/v1/'
basic_auth = ('ehrbase-user', 'SuperSecretPassword')

# Send a POST message to the openEHR server in order to execute a query. The
# message contains a JSON query with the following format:
# { "q" : {query-content} }

def execute_query(query):
    url = openEHR_baseURL + 'query/aql'
    headers = {
        'content-type' : 'application/json',
        'prefer' : 'return=representation'
    }
    return requests.post(url, data = str(json.dumps(query)), headers = headers,
        auth= basic_auth)

# Send a POST message to the openEHR server containing the composition to
# upload.

def upload_composition(composition, patient_ID):
    url = openEHR_baseURL + 'ehr/' + patient_ID + '/composition'
    headers = {
       'content-type': 'application/json',
       'prefer' : 'return=representation'
    }

    formatted_composition = str(composition).replace('\'', '\"')
    return requests.post(url, data = formatted_composition, headers = headers, auth = basic_auth)

# Send a PUT message to the openEHR server containing the updated composition
# to upload.

def update_composition(composition, patient_ID, complete_ID):
    brief_ID = str(complete_ID).split('::', 1)[0]
    url = openEHR_baseURL + 'ehr/' + patient_ID + '/composition/' \
        + brief_ID
    headers = {
       'content-type': 'application/json',
       'prefer' : 'return=representation',
       'If-Match' : complete_ID
    }
    return requests.put(url, data = str(composition).replace('\'', '\"') \
        .replace("False", 'false'), headers = headers, auth= basic_auth)
