import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime
import database
import plotly.express as px

# ==> SUPPORT DASHBOARD PAGE FOR MANAGING QUERIES..

def support_dashboard():
    st.header(":blue[_QUERY MANAGEMENT..._]📄")

    conn = database.db_connection()
    cursor = conn.cursor()
    
    col1,col2,col3= st.columns(3)

    status = col1.selectbox("Select Status:",['All','Open','Closed'])
    query_category = col2.selectbox("Query Category:",
                                 ['None','Account Suspension','Billing Problem','Bug Report','Data Export',
                                  'Feature Request','Login Issue','Payment Failure','Subscription Cancellation',
                                  'Technical Support','UI Feedback'])
    if status == 'All' and query_category == 'None':
        query = """
                SELECT * FROM queries 
                ORDER BY query_created_time DESC
                """
        cursor.execute(query)
    
    elif status == 'All' and query_category != 'None':
        query = """
                SELECT * FROM queries
                WHERE query_heading = %s 
                ORDER BY query_created_time DESC
                """
        data = (query_category,)
        cursor.execute(query,data)
    
    elif status != 'All' and query_category == 'None':
        query = """
                SELECT * FROM queries
                WHERE status = %s
                ORDER BY query_created_time DESC
                """
        data = (status,)
        cursor.execute(query,data)
    
    else:
        query = """
                SELECT * FROM queries
                WHERE status = %s AND query_heading = %s
                ORDER BY query_created_time DESC
                """
        data = (status,query_category)
        cursor.execute(query,data)

    queries = cursor.fetchall()
    df = pd.DataFrame(queries,columns=['query_id','client_email','client_mobile','query_heading','query_description','status','query_created_time','query_closed_time'])
    st.dataframe(df,hide_index=True)

    # ==> CLOSE OPEN QUERY BY USING QUERY ID..

    if status == 'Open':
        open_query_id = [i[0] for i in queries if i[5] == "Open"]

        if open_query_id:
            close_query = col3.selectbox("Select Query ID to close:",open_query_id)

            close_button = col3.button("Close Query")

            if close_button:
                query = """
                        UPDATE queries
                        SET status = 'Closed', query_closed_time = %s
                        WHERE query_id = %s
                        """
                data = (datetime.now(),close_query)
                cursor.execute(query,data)
                conn.commit()

                st.success(f"Query ID: {close_query} Closed successfully..")

    chart1_toggle = st.toggle("_Show **Query Category** Distribution Chart_")
    
    cursor.execute("SELECT query_heading FROM queries") 
    que_head = cursor.fetchall()

    df_head = pd.DataFrame(que_head, columns=["query_heading"])
    
    if chart1_toggle:
        chart = px.pie(df_head, names= 'query_heading', title= 'Query Category Distribution')
        chart.update_traces(hovertemplate= '%{label}')
        st.plotly_chart(chart)           
        

    chart2_toggle = st.toggle("_Show **Query Status** Distribution Chart_")
    
    cursor.execute("SELECT status FROM queries") 
    st_data = cursor.fetchall()

    df_head = pd.DataFrame(st_data, columns=["status"])
    
    if chart2_toggle:
        chart = px.pie(df_head, names= 'status', title= 'Query Status Distribution')
        chart.update_traces(hovertemplate= '%{label}')
        st.plotly_chart(chart)           
        conn.close()
