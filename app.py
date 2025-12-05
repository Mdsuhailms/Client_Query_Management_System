import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import client, support, login_page




# ==> HOME PAGE..

st.set_page_config(page_title="Client Query Management System", layout="centered", initial_sidebar_state= "expanded")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.current_page = "home"


with st.sidebar:
    if st.session_state.logged_in:
        
        if st.session_state.role == "client":
            pages = ["Home", "Client", "Logout"]
            icons = ["house-fill", "person-circle", "box-arrow-left"]

        elif st.session_state.role == "support":
            pages = ["Home", "Support Dashboard", "Logout"]
            icons = ["house-fill", "tools", "box-arrow-left"]

        else:
            pages = ["Home", "Logout"]
            icons = ["house-fill", "box-arrow-left"]

        page_selection = option_menu(
            menu_title=None,
            options=pages,
            icons=icons
        )

        if page_selection == 'Home':
            st.session_state.current_page = "home"

        elif page_selection == 'Client':
            st.session_state.current_page = "client"

        elif page_selection == 'Support Dashboard':
            st.session_state.current_page = "support"

        elif page_selection == 'Logout':
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.current_page = "home"
            st.session_state.login_success = False
            st.rerun()
    
    else:
        option_menu(
                menu_title= None,
                options= ['Home'],
                icons=['house-fill']
        )
 

if st.session_state.current_page == "home":
    login_page.home()

elif st.session_state.current_page == "client":
    if st.session_state.logged_in and st.session_state.role == 'client':
        client.submit_query()

elif st.session_state.current_page == "support":
    if st.session_state.logged_in and st.session_state.role == 'support':
        support.support_dashboard()
    

            

