from flask import Flask
from flask import request, escape
from flask import render_template

import aql_query as query_builder
import openEHR_handler as openEHR
import context_handler as context
import db as demographics
import application_handler as app_handler
import mysql.connector
import json

app = Flask(__name__)
EMPTY_COMPOSITION_MSG = "The submitted composition has probably empty content. Check your form again."
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "demographics"
)

@app.errorhandler(500)
def page_internal_error(e):
    # note that we set the 404 status explicitly
    return json.dumps("Composition structure error. Check composition syntax before upload."), 500

def get_archetype_id(arch):
     arch_details = arch['archetype_details']
     arch_id = arch_details['archetype_id']
     return arch_id['value']

@app.route("/composition/encounter", methods = ["POST"])
def enforce_reason_for_encounter_creation():
  subject_req = request.get_json()

  arch_ID = subject_req['attributes']['resource']['archetype-id']
  if arch_ID['value'] == 'encounter':
      arch_ID['value'] = 'openEHR-EHR-COMPOSITION.encounter.v1'
  else:
      return app_handler.send_message("Wrong composition name.")

  # Creation and transmission of the XACML request to the PEP

  attributes = subject_req['attributes']
  xacml_request = context.create_xacml_request(attributes)
  xacml_response = context.send_XACML_request_to_PEP(xacml_request)

  if context.read_xacml_decision(xacml_response) != 'Permit':
     return app_handler.send_negative_response_to_app()

  # Enforcing the following obligation: the Encounter composition created by
  # the administration staff must contain only the Reason for Encounter
  # archetype, i.e this subject is not allowed to create any other archetypes
  # apart from that.

  encounter = subject_req['composition']
  if(len(encounter) == 0):
      return EMPTY_COMPOSITION_MSG

  arch_list = encounter['content']
  reason_for_encounter_arch = arch_list[0]
  archetype_ID = get_archetype_id(reason_for_encounter_arch)
  obligation_archetype_ID = context.read_obligation(xacml_response)[0]

  if len(arch_list) != 1 or archetype_ID != obligation_archetype_ID:
     return app_handler.send_negative_response_to_app()

  # Upload the Encounter composition to patient's EHR
  ehr_ID = subject_req["attributes"]["resource"]["ehr-id"]["value"]
  openEHR_response = openEHR.upload_composition(encounter, ehr_ID)
  return app_handler.send_composition_to_app(openEHR_response.text)

@app.route("/composition/encounter/vital_signs", methods = ["PUT"])
def enforce_add_vital_signs_to_encounter():
    subject_req = request.get_json()
    arch_ID = subject_req['attributes']['resource']['archetype-id']

    # Is the composition carried in the request related to encounter?
    if arch_ID['value'] == 'encounter':
        arch_ID['value'] = 'openEHR-EHR-COMPOSITION.encounter.v1'
    else:
        return app_handler.send_message("Wrong composition name.")

    # Creation and transmission of the XACML request to PDP
    attributes = subject_req['attributes']
    xacml_request = context.create_xacml_request(attributes)
    xacml_response = context.send_XACML_request_to_PEP(xacml_request)

    if context.read_xacml_decision(xacml_response) != 'Permit':
        return app_handler.send_negative_response_to_app()

    # We don't want do upload any empty composition
    if(len(subject_req['composition']) == 0):
        return app_handler.send_message("Composition cannot be empty.")

    # Extract the subtree to attach to the encounter tree
    subtree = subject_req['composition']
    arch_type = subtree['archetype_details']['archetype_id']['value']

    # Obligation: verify the subtree is of the vitals type
    if arch_type != context.read_obligation(xacml_response)[0]:
        return app_handler.send_negative_response_to_app()

    # Retrieve the encounter identifier from the demographic repository
    ehr_ID = subject_req["attributes"]["resource"]["ehr-id"]["value"]
    ref_ID = subject_req["attributes"]["subject"]["random-id"]["value"]
    comp_ID = demographics.retrieve_composition_id(ref_ID, ehr_ID)

    # Retrieve the encounter tree from the openEHR repository
    comp_type = "openEHR-EHR-COMPOSITION.encounter.v1"
    query = query_builder.retrieve_composition2(comp_type, comp_ID)
    query_result = openEHR.execute_query(query)
    tree = query_result.json()["rows"][0][0]

    # Attach the subtree to the encounter tree and upload it all to the
    # updated encounter to the openEHR repository
    tree['content'].append(subtree)
    response = openEHR.update_composition(tree, ehr_ID, comp_ID)
    return app_handler.send_positive_response_to_app()

@app.route("/composition/encounter/diagnosis", methods = ["PUT"])
def enforce_add_diagnosis_to_encounter():
    subject_req = request.get_json()
    arch_ID = subject_req['attributes']['resource']['archetype-id']

    # Is the composition carried in the request related to medication list?
    if arch_ID['value'] == 'encounter':
        arch_ID['value'] = "openEHR-EHR-COMPOSITION.encounter.v1"
    else:
        return app_handler.send_message("Wrong composition name.")

    # Creation and transmission of the XACML request to the PEP
    attributes = subject_req['attributes']
    xacml_request = context.create_xacml_request(attributes)
    xacml_response = context.send_XACML_request_to_PEP(xacml_request)

    if context.read_xacml_decision(xacml_response) != 'Permit':
        return app_handler.send_negative_response_to_app()

    # We don't want do upload any empty composition
    if(len(subject_req['composition']) == 0):
        return app_handler.send_message("Composition cannot be empty.")

    # Enforcing the following obligation: the internist is allowed to update the
    # Encounter composition with the Problem/Diagnosis archetype.
    subtree = subject_req['composition']
    arch_type = subtree['archetype_details']['archetype_id']['value']

    if arch_type != context.read_obligation(xacml_response)[0]:
        return app_handler.send_negative_response_to_app()

    # To update the Encounter composition, its latest version must be
    # retrieved from the openEHR first. For this, a query is prepared and
    # executed.

    ehr_ID = subject_req["attributes"]["resource"]["ehr-id"]["value"]
    ref_ID = subject_req["attributes"]["subject"]["random-id"]["value"]
    comp_ID = demographics.retrieve_composition_id(ref_ID, ehr_ID)

    query = query_builder.retrieve_composition(arch_ID['value'], ehr_ID)
    query_result = openEHR.execute_query(query)
    tree = query_result.json()["rows"][0][0]

    # Update the Encounter composition by appending the Problem/Diagnosis archetype.
    tree['content'].append(subtree)

    # Send an update message to openEHR server.

    tree_ID = tree['uid']['value']
    openEHR_response = openEHR.update_composition(tree, ehr_ID, comp_ID)
    return app_handler.send_positive_response_to_app()

@app.route("/composition/<composition>", methods = ["GET"])
def enforce_read_composition(composition):
  subject_req = request.get_json()

  # Escape permalink for security reasons
  composition_name = escape(composition)

  # Check if the requested composition is of one of the types below.
  allowed_names = {
    "medication_list" : "openEHR-EHR-COMPOSITION.medication_list.v1",
    "allergy_list" : "openEHR-EHR-COMPOSITION.adverse_reaction_list.v1",
    "encounter" : "openEHR-EHR-COMPOSITION.encounter.v1"
  }

  # Replace the archetype-id JSON member with the standard one.
  if composition_name in allowed_names.keys():
      comp_type = allowed_names[composition_name]
  else:
      return app_handler.send_negative_response_to_app()

  attributes = subject_req['attributes']
  attributes['resource']['archetype-id'] = {
     "type" : "string", "value" : comp_type, "xacmlns" : "false"
  }

  # JSON attributes submitted by the user are mapped to XACML elements
  # by context handler.
  xacml_request = context.create_xacml_request(attributes)
  xacml_response = context.send_XACML_request_to_PEP(xacml_request)

  if context.read_xacml_decision(xacml_response) != 'Permit':
     return app_handler.send_negative_response_to_app()

  # Retrieving the ref-id from the demographics repository
  ehr_ID = subject_req["attributes"]["resource"]["ehr-id"]["value"]
  ref_ID = subject_req["attributes"]["subject"]["random-id"]["value"]
  field = context.read_obligation(xacml_response)[0]
  encounter_ID = demographics.retrieve_field(field, ref_ID, ehr_ID)

  # Retrieving the ref-id from the encounter composition contained in
  # the openEHR repository
  query = query_builder.retrieve_composition_field(
    "c/composer/external_ref/id/value",
    "openEHR-EHR-COMPOSITION.encounter.v1",
    encounter_ID
  )
  response_openEHR = openEHR.execute_query(query)
  encounter_ref_ID =  response_openEHR.json()["rows"][0][0]

  # Obligation 1: check if the requester is the physician in
  # charge of the encounter
  if encounter_ref_ID != ref_ID:
     return app_handler.send_negative_response_to_app()

  # Execute query against the openEHR repository to get the composition
  # requested
  phys_query = query_builder.retrieve_composition(comp_type, ehr_ID)
  req_composition = openEHR.execute_query(phys_query)
  return app_handler.send_pretty_composition_to_app(req_composition)

@app.route("/composition/medication_list", methods = ["PUT"])
def enforce_add_new_medication_order():
    subject_req = request.get_json()
    arch_ID = subject_req['attributes']['resource']['archetype-id']

    # Is the composition carried in the request related to medication list?
    if arch_ID['value'] == 'medication_list':
        arch_ID['value'] = 'openEHR-EHR-COMPOSITION.medication_list.v1'
    else:
        return app_handler.send_message("Wrong composition name.")

    # Creation and transmission of the XACML request to PDP
    attributes = subject_req['attributes']
    xacml_request = context.create_xacml_request(attributes)
    xacml_response = context.send_XACML_request_to_PEP(xacml_request)

    # Check if the policy evaluation is successful
    if context.read_xacml_decision(xacml_response) != 'Permit':
        return app_handler.send_negative_response_to_app()

    # We don't want any empty composition to upload
    if(len(subject_req['composition']) == 0):
        return str("Composition cannot be empty.")

    # Retrieve the encounter identifier stored in the demographics repository
    ehr_ID = attributes["resource"]["ehr-id"]["value"]
    ref_ID = attributes["subject"]["random-id"]["value"]
    field = context.read_obligation(xacml_response)[0]
    encounter_ID = demographics.retrieve_field(field, ref_ID, ehr_ID)

    # Retrieve the identifier of the physician in charge of the
    # encounter from the openEHR repository
    query = query_builder.retrieve_composition_field(
      "c/composer/external_ref/id/value",
      "openEHR-EHR-COMPOSITION.encounter.v1",
      encounter_ID
    )
    response_openEHR = openEHR.execute_query(query)
    encounter_ref_ID =  response_openEHR.json()["rows"][0][0]

    # Obligation 1: check if the requester is the physician responsible for
    # the encounter.
    if encounter_ref_ID != ref_ID:
       return app_handler.send_negative_response_to_app()

    # Obligation 2: the archetype to upload must be of the medication order type.
    subtree = subject_req['composition']
    archetype_id = subtree['archetype_details']['archetype_id']['value']

    if archetype_id != context.read_obligation(xacml_response)[1]:
        return app_handler.send_negative_response_to_app()

    # Retrieve the latest version of the Medication list composition.
    query = query_builder.retrieve_composition(arch_ID['value'], ehr_ID)
    query_result = openEHR.execute_query(query)
    tree = query_result.json()["rows"][0][0]
    medication_order_list_arch = tree['content'][0]

    # If the medication list is empty, the "items" entry is missing
    # and therefore needs to be created to contain the new medication and all the
    # future ones.
    if "items" not in medication_order_list_arch.keys():
        medication_order_list_arch["items"] = [subtree]
    else:
        medication_order_list_arch["items"].append(subtree)

    # A PUT http call is created to upload the updated medication list
    # composition with the new medication order.
    tree_ID = tree['uid']['value']
    openEHR_response = openEHR.update_composition(tree, ehr_ID, tree_ID)
    return app_handler.send_positive_response_to_app()
