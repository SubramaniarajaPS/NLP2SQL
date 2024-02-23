from dotenv import load_dotenv
load_dotenv() #load all the environment variables
import streamlit as st
import os
import sqlite3
import google.generativeai as genAI

# API Key Configuration
genAI.configure(api_key = os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Model which gives SQL Queries as response
def get_gemini_response(question,prompt): 
  model = genAI.GenerativeModel('gemini-pro') # Choosing the desired model
  response = model.generate_content([prompt[0],question]) 
  return response.text

# Function to retrieve Query from SQL DB
def read_sql_query(sql,db):
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
  The SQL database has the table name MAP and has the following column - WARNING, DTC, FAILURE, CAUTION and SEVERITY. \n\nFor example,\nExample 1 - How many entries of records are present?, 
  the SQL command will be something like this SELECT COUNT(*) FROM MAP;
  \nExample 2 - Tell me all the entries from records having SEVERITY 1 ?, the SQL command will be something like this SELECT * FROM MAP where SEVERITY=1;
  also the sql code should not have ``` in beginning or end of the sql word in the output
  
  """
]  

# For Streamlit UI 
st.set_page_config(page_title = "NLP to SQL query")
st.header("MAP QUERIES")

question = st.text_input("Input: ",key="input")

submit = st.button("Submit")

# If submit is clicked
if submit:
    response = get_gemini_response(question,prompt)
    print(response)
    data = read_sql_query(response,"map.db")
    st.subheader("The Response is ")
    for row in data:
        print(row)
        st.header(row)