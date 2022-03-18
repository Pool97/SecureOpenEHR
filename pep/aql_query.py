# Create a dict with the composition to be retrieved from a specific
# patient's EHR.

def retrieve_composition(composition_ID, patient_ID):
    projection_clause = "SELECT c from EHR e "
    contains_clause = "CONTAINS COMPOSITION c[" + composition_ID + "] "
    selection_clause = "WHERE e/ehr_id/value = \'" + patient_ID + "\'"
    return {"q" : projection_clause + contains_clause + selection_clause}

def retrieve_composition2(composition_type, composition_ID):
    projection_clause = "SELECT c from EHR e "
    contains_clause = "CONTAINS COMPOSITION c[" + composition_type + "] "
    selection_clause = "WHERE c/uid/value = \'" + composition_ID + "\'"
    return {"q" : projection_clause + contains_clause + selection_clause}

# Create a dict with a composition field to be retrieved from a specific
# patient's EHR.

def retrieve_composition_field(field, composition_type, composition_ID):
    projection_clause = "SELECT " + field + " from EHR e "
    contains_clause = "CONTAINS COMPOSITION c[" + composition_type + "] "
    selection_clause = "WHERE c/uid/value = \'" + composition_ID + "\'"
    return {"q" : projection_clause + contains_clause + selection_clause}
