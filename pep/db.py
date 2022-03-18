import mysql.connector
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "demographics"
)
def retrieve_composition_id(reference_id, ehr_id):
    mycursor = mydb.cursor()
    parameters = (reference_id, ehr_id)
    mycursor.execute("SELECT composition_id FROM carestaff WHERE reference_id = %s and EHR_id = %s", parameters)
    return mycursor.fetchone()[0] #[0]

def retrieve_field(field, reference_id, ehr_id):
    mycursor = mydb.cursor()
    parameters = (reference_id, ehr_id)
    mycursor.execute("SELECT " + field + " FROM carestaff WHERE reference_id = %s and EHR_id = %s", parameters)
    return mycursor.fetchone()[0] #[0]
