from lxml import etree
import requests

authzforce_baseURL = 'http://localhost:8081/authzforce-ce/'
permalink_PDP = 'domains/UKwAXJV-Eey6oQJCrBEAAg/pdp'

# A XACML request has normally the following format:
#
# <Request xmlns = ... CombinedDecision = ... ReturnPolicyIdList = ...>
#   <Attributes Category = ...>
#      <Attribute AttributeId = ... IncludeInResult = ...>
#          <AttributeValue>     </AttributeValue>
#       </Attribute>
#   </Attributes>
#    ...
# </Request>
#

def create_xacml_request(attributes_list):

    # Default value for attributes of the root element are set. They can
    # be customized depending on your needs.

    Request_attributes = {
        "xmlns" : "urn:oasis:names:tc:xacml:3.0:core:schema:wd-17",
        "CombinedDecision" : "false",
        "ReturnPolicyIdList" : "false"
    }

    RequestElement = etree.Element('Request', attrib = Request_attributes)

    # Standard categories of attributes are specified with their namespaces.

    categories = ['subject', 'resource', 'action', 'environment']

    categories_namespace = {
        'subject' : "urn:oasis:names:tc:xacml:1.0:subject-category:access-subject",
        'resource' : "urn:oasis:names:tc:xacml:3.0:attribute-category:resource",
        'action' : "urn:oasis:names:tc:xacml:3.0:attribute-category:action",
        'environment' : "urn:oasis:names:tc:xacml:3.0:attribute-category:environment"
    }

    attributes_namespace = {
        'subject' : "urn:oasis:names:tc:xacml:1.0:subject",
        'resource' : "urn:oasis:names:tc:xacml:1.0:resource",
        'action' : "urn:oasis:names:tc:xacml:1.0:action",
        'environment' : "urn:oasis:names:tc:xacml:1.0:environment"
    }

    for category in categories:

        # Creation of the <Attributes> subelement for the <Request> element
        AttributesElement = etree.SubElement(RequestElement, 'Attributes',
            attrib = {"Category" : categories_namespace[category]})

        # Creation of all the XML attributes that fall under the same category
        for attribute, value in attributes_list[category].items():

            # Definition of the <Attribute> element and its inclusion in the
            # XACML request as a child of <Attributes> element. Both standard
            # and custom attributes can be created. The boolean property "xacmlns"
            # contained in the application request distinguishes these cases.

            attributes = {
                "AttributeId" : attribute if value['xacmlns'] == "false"
                    else attributes_namespace[category] + ':' + attribute,
                "IncludeInResult" : "true"
            }

            AttributeElement = etree.SubElement(AttributesElement, 'Attribute',
                attrib = attributes)

            # Creation of the <AttributeValue> subelement for the <Attribute>
            # element.

            AttributeValue_attributes = {
                "DataType" : "http://www.w3.org/2001/XMLSchema#" + value['type']
            }

            attributeValueElement = etree.SubElement(AttributeElement,
                'AttributeValue', attrib = AttributeValue_attributes)
            attributeValueElement.text = value['value']

    xacml_request_string = etree.tostring(RequestElement, pretty_print = True,
        xml_declaration = True, encoding='UTF-8').decode()
    print_xacml_request(xacml_request_string)
    return xacml_request_string

# A XACML request is sent to the PDP according to the Authzforce API.
def send_XACML_request_to_PEP(xacml_request):
    url = authzforce_baseURL + permalink_PDP
    headers = {'content-type' : 'application/xml'}
    return requests.post(url, data = xacml_request, headers = headers)

# A XACML response has normally the following format:
#
# <Response xmlns = ...>
#   <Result>
#      <Decision> Permit </Decision>
#      <Obligations>
#          <Obligation ObligationId = ...>
#              <AttributeAssignment AttributeId = ... DataType = ...>
#                   ...
#              </AttributeAssignment>
#          </Obligation>
#          ...
#      </Obligations>
#   </Result>
# </Response>

# Read the value contained in the <Decision> element of the XACML response.
def read_xacml_decision(xacml_response):
    print(xacml_response.text)
    tree = etree.fromstring(bytes(xacml_response.text, encoding = 'utf-8'))
    child = tree.xpath('//ns3:Decision',  namespaces={'ns3': 'urn:oasis:names:tc:xacml:3.0:core:schema:wd-17'})
    print_xacml_response(xacml_response)
    return child[0].text

# Read all of the obligations contained in the <Obligations> element of the
# XACML response. Put each value in a list that will be returned by this
# function.

def read_xacml_attribute_from_response(xacml_response, attribute_id):
    tree = etree.fromstring(bytes(xacml_response.text, encoding = 'utf-8'))
    child = tree.xpath('//ns3:Attributes', namespaces={'ns3': 'urn:oasis:names:tc:xacml:3.0:core:schema:wd-17'})

    element =  tree.xpath('//ns3:Attributes[@Category="urn:oasis:names:tc:xacml:1.0:subject-category:access-subject"]//ns3:Attribute[@AttributeId="random-id"]//ns3:AttributeValue', namespaces={'ns3': 'urn:oasis:names:tc:xacml:3.0:core:schema:wd-17'})
    return element[0].text

def read_obligation(xacml_response):
    tree = etree.fromstring(bytes(xacml_response.text, encoding = 'utf-8'))
    ObligationsElement = tree[0][1]
    response_attributes = []

    print(ObligationsElement)
    for Obligation in ObligationsElement:
        for AttributeAssignment in Obligation:
            response_attributes.append(AttributeAssignment.text)
    return response_attributes

def print_xacml_request(xacml_request):
    print("\nXACML REQUEST FROM PDP TO PEP\n")
    print(xacml_request)

def print_xacml_response(xacml_response):
    tree = etree.fromstring(bytes(xacml_response.text, encoding = 'utf-8'))
    print("\nXACML RESPONSE FROM PEP to PDP\n")
    print(etree.tostring(tree, pretty_print = True,
        xml_declaration = True, encoding='UTF-8').decode())
