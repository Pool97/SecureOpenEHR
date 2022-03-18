import json

# Send a JSON composition to the application after going through a JSON
# formatter.

def send_pretty_composition_to_app(composition):
    return str(json.dumps(composition.json()["rows"][0][0], indent = 4))

def send_composition_to_app(composition):
    return str(composition)

def send_message(message):
    return str(message)

def send_composition_structure_error():
    return 'Error, Composition structure is not correct'

def send_positive_response_to_app():
    return 'Request executed successfully.'

def send_negative_response_to_app():
    return 'Request not executed due to lack of privilege'
