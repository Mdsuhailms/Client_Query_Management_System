import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import hashlib
from datetime import datetime
import database


# ==> HASHING PASSWORD..

def password_hashing(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ==> LOGIN/REGISTER PAGE..

def home():
    st.title(":grey[Client Query Management]📝")

    if st.session_state.get("logged_in") and st.session_state.get("login_success"):
        if st.session_state.role == 'client':
            st.success("Logged in as **CLIENT**..Navigate using Sidebar..!!")
        
        else:
            st.success("Logged in as **SUPPORT TEAM**..Navigate using Sidebar..!!")

        
    tab = option_menu(
        menu_title= None,
        options= ["Login", "Register"],
        icons= ["box-arrow-in-right","person-vcard-fill"],
        orientation= "horizontal",
    )
    
    if tab == "Login":

        username = st.text_input("Username:")
        password = st.text_input("Password:",type="password")

        hash_password = password_hashing(password)
        
        login = st.button("Login")

        if login:
            if username.strip() == "" or password.strip() == "":
                st.warning("Please Enter both Username and Password..!!")
                return
            
            
            conn = database.db_connection()
            cursor = conn.cursor()

            query = """
                    SELECT role FROM users
                    WHERE username = %s AND hashed_password = %s
                    """
            data = (username,hash_password)

            cursor.execute(query,data)
            result = cursor.fetchone()
            conn.close()

            
            if result:
                
                role = result[0]

                st.session_state.logged_in = True
                st.session_state.role = role
                st.session_state.login_success = True
                
                if role == 'client':
                    st.session_state.current_page = 'client'
                
                else:
                    st.session_state.current_page = 'support'
                
                st.rerun()
            
            else:
                st.error("Invalid Username or Password")


    # ==> USER REGISTRATION..

    if tab == "Register":
        st.subheader("Enter Your Details.")

        new_user = st.text_input("Create Username:")
        new_password = st.text_input("Create Password:",type="password")
        new_role = st.selectbox("Select Role:(Client/Support)", ["client", "support"])

        register = st.button("Register")

        reg_hash_password = password_hashing(new_password)

        if register:
            if new_user.strip() == "" or new_password.strip() == "":
                st.warning("Please Enter both Username and Password..!!")
                return
            
            conn = database.db_connection()
            cursor = conn.cursor()

            query = """
                    INSERT INTO users(username,hashed_password, role)
                    VALUES(%s, %s, %s)
                    """
            data = (new_user, reg_hash_password, new_role)

            cursor.execute(query,data)
            conn.commit()
            conn.close()

            st.success("Registeration Successful..!! You can Login now..")



