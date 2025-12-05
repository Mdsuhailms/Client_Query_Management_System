import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime
import database

# ==> TO GENERATE QUERY ID'S FOR SUBMITTING QUERIES..

def generate_next_query_id():
    conn = database.db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT query_id FROM queries ORDER BY query_id DESC LIMIT 1")
    query_row = cursor.fetchone()

    conn.close()

    if not query_row:
        return "Q0001"

    last_query_id = query_row[0]        
    number = int(last_query_id[1:])   
    add_query = number + 1

    return f"Q{add_query:04d}"

# ==> SUBMITTING QUERY..

def submit_query():
    st.header(":grey[_SUBMIT YOUR QUERY.._]💬")

    email = st.text_input("Email ID:")
    mobile = st.text_input("Mobile Number:")
    query_heading = st.selectbox("Query Heading:",
                                 ['Account Suspension','Billing Problem','Bug Report','Data Export',
                                  'Feature Request','Login Issue','Payment Failure','Subscription Cancellation',
                                  'Technical Support','UI Feedback'])
    query_desc = st.text_area("Query Description:")

    submit = st.button("Submit Query")

    if submit:
        if email.strip() == "" or mobile.strip() == "" or query_desc.strip() == "":
                st.warning("Fill All the Details before Submitting..!!")
                return
        
        conn = database.db_connection()
        cursor = conn.cursor()

        query_id = generate_next_query_id()
        created_time = datetime.now()

        query = """
                INSERT INTO queries(query_id,client_email,client_mobile,query_heading,query_description,status,query_created_time,query_closed_time)
                VALUES(%s, %s, %s, %s, %s, 'Open',%s, %s)
                """
        data = (query_id,email,mobile,query_heading,query_desc,created_time,None)

        cursor.execute(query,data)
        conn.commit()
        conn.close()

        st.success("Query Submitted Successfully...!!")
        



