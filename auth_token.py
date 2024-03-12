import os
import requests
import sqlite3
import streamlit as st




#  < - INITIALIZATION OF CONFIGURATION VARIABLES - >  #

token_endpoint = "https://login.microsoftonline.com/c990bb7a-51f4-439b-bd36-9c07fb1041c0/oauth2/v2.0/token"
api_host = "api.pd01i.gcp.ford.com"
api_endpoint = "https://api.pd01i.gcp.ford.com/llm/api/chat"
proxy_endpoint = "http://internet.ford.com:83"
scope = "api://0c646856-16de-4604-86f6-ddeaa039a541/.default"

client_id = "ab07db28-3f02-4831-b38e-b2eba96c0d0e"
client_secret = "~Pf8Q~4iwFGtFst2Ee3vmn0TpHEYlGFHlYzzrbJ7"

os.environ['HTTP_PROXY'] = proxy_endpoint
os.environ['HTTPS_PROXY'] = proxy_endpoint
os.environ['NO_PROXY'] = api_host

token = None



#  < - TO GET FORD LLM AZURE TOKEN FOR AUTHENTICATION - >  #
 
def get_token():
    response = requests.post(token_endpoint, data={
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope,
        "grant_type": "client_credentials"
    })

    return response.json()['access_token']

token = get_token()

print(" \n \n >>>>> AZURE BEARER TOKEN : \n \n " + token + "\n \n")

if not token:
    print('Cannot acquire token.')
    exit()



#  < - QUESTION ASKED TO LLM - >  #

st.set_page_config(page_title = "NLP to SQL query")
st.header(" DTS AI - NLP2SQL RAG LLM ")
question = st.text_input("Input: ", key = "input")


print("\n >>>>> NLP QUESTION ASKED TO LLM : \n \n"+ question + "\n \n")



#  < - CONFIGURATION OF LLM INPUT - >  #

def call_api(token):
    response = requests.post(api_endpoint,
    headers={
        "Authorization": f"Bearer {token}"
    },
    json={
        "model": "gpt-4",
        "context": "You are the world's best expert in converting the natural language english questions into SQL Queries! \n" +
        "The DTS SQL database has the two tables named as MAP and LANG.\n"+
        "The MAP table from DTS database has the following columns - MAPKEY, WARNING, DTC, FAILURE, CAUTION and SEVERITY.\n"+
        "Also the sql query should not have```sql in beginning and ```in the end for the output",
        "examples": [
            {
              "input": "How many entries of records are present in MAP table?",
              "output": "SELECT COUNT(*) FROM MAP;"
            },
            {
              "input": "Tell me all the entries from the MAP table records having SEVERITY 1 ?",
              "output": "SELECT * FROM MAP where SEVERITY=1;" 
            },
            {
              "input": "Give me the record from LANG table that has mapkeys equal to 1 and 2?",
              "output": "SELECT * FROM LANG where MAPKEY in(1,2);" 
            },
            {
              "input": "Give all the language and country for the particular warning, dtc and failure?",
              "output": "SELECT MAP.WARNING, MAP.DTC, MAP.FAILURE, LANG.COUNTRY, LANG.LANGUAGE FROM MAP JOIN LANG ON MAP.MAPKEY = LANG.MAPKEY;" 
            }
          ],     
        "messages": [{
            "role": "user",
            "content": question
        }],
        "parameters": {
            "temperature": 0.7,
            "maxOutputTokens": 400
        }
    })

    print(response.json())

    return response.json()['content']



#  < - CONFIGURATION OF LLM OUTPUT - >  #

response = call_api(token)
print("\n \n >>>>> SQL QUERY FROM LLM FOR GIVEN LLM IS : \n \n " + response + "\n \n")



#  < - QUERYING WITH THE LLM GENERATED SQL QUERY FOR THE CONNECTED DB - >  #

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    print(" \n >>>> THE RESULT SET OUTPUT FROM DB IS : \n  ")
    for row in rows:
        print(row)
    print("  \n  ")
    return rows



#  < - STREAMLIT FOR UI - >  #

submit = st.button(" SUBMIT ")
if submit:
    data = read_sql_query(response, "DTS.db")
    st.subheader(" The Following Is The Output Result Set ")
    for row in data:
        print(row)
        st.header(row)



