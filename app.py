from dotenv import load_dotenv

load_dotenv()  # load all the environment variables
import streamlit as st
import os
import sqlite3
import google.generativeai as genAI
import auth_token as auth

# API Key Configuration
genAI.configure(api_key = auth.get_token)


# Function to load Google Gemini Pro Model which gives SQL Queries as response
def get_gemini_response(question, prompt):
    model = genAI.GenerativeModel('gemini-pro')  # Choosing the desired model
    response = model.generate_content([prompt[0], question])
    return response.text


# Function to retrieve Query from SQL DB
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows


# Define the Prompt
prompt = [
    """
    You are the world's best expert in converting the natural language english questions into SQL Queries! \n
    The DTS SQL database has the two tables named as MAP and LANG.
    The MAP table from DTS database has the following columns - MAPKEY, WARNING, DTC, FAILURE, CAUTION and SEVERITY.\n
    The LANG table from DTS database has the following columns - LANGLOCALEKEY, COUNTRY, LANGUAGE, LOCALE, MAPKEY.\n
    From the MAP table, if the given input has something similar to 600E00, then consider it as a record of WARNING.
    From the MAP table, if the given input has something similar to 0000, then consider it as a record of DTC.
    From the MAP table, if the given input  has something similar to 11, then consider it as a record of FAILURE.
    From the MAP table, if the given input length is 100 , then consider it as CAUTION.
    \nFor example,\nExample 1 - How many entries of records are present in MAP table?,
    the SQL command will be something like this SELECT COUNT(*) FROM MAP;
    \nExample 2 - Tell me all the entries from the MAP table records having SEVERITY 1 ?, the SQL command will be something like this SELECT * FROM MAP where SEVERITY=1;
    \nFor example,\nExample 3 - Give me the record from LANG table that has mapkeys equal to 1 and 2,
    the SQL command will be something like this SELECT * FROM LANG where MAPKEY in(1,2);
    \nFor example,\nExample 4 - Give all the language and country for the particular warning,dtc and failure ,
    the SQL command will be something like this SELECT MAP.WARNING, MAP.DTC, MAP.FAILURE, LANG.COUNTRY, LANG.LANGUAGE FROM MAP JOIN LANG ON MAP.MAPKEY = LANG.MAPKEY;
    also the sql code should not have``` in beginning or end of the sql word in the output
  """
]

# For Streamlit UI
st.set_page_config(page_title="NLP to SQL query")
st.header("DTS QUERIES")

question = st.text_input("Input: ", key="input")

submit = st.button("Submit")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(question)
    print(response)
    data = read_sql_query(response, "DTS.db")
    st.subheader("THE DESIRED RESPONSE IS ")
    for row in data:
        print(row)
        st.header(row)
