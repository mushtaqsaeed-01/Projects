import streamlit as st
import json
from Admin import Admin
from User import User


admin_var = Admin()
user_var = User()

if "Name_of_User" not in st.session_state:
    st.session_state.Name_of_User = ""

if "id_of_user" not in st.session_state:
    st.session_state.id_of_user = 0

if "signup" not in st.session_state:
    st.session_state.signup = True

if "login" not in st.session_state:
    st.session_state.login = False

if "admin_state" not in st.session_state:
    st.session_state.admin_state = False

if "user_state" not in st.session_state:
    st.session_state.user_state = False

if "is_login" not in st.session_state:
    st.session_state.is_login = False


def admin():
    st.sidebar.title(":material/manage_accounts: Admin Panel")
    menu_for_admin = st.sidebar.selectbox("Select Action",["All Books", "Add Book", "Remove Book", "Borrowed Books", "Search Book", "Search User"])
    
    match menu_for_admin:
        case "Add Book":
            admin_var.add_book()

        case "Remove Book":
            admin_var.remove_book()

        case "All Books":
            admin_var.show_books()

        case "Borrowed Books":
            admin_var.borrowed_books()

        case "Search Book":
            admin_var.search_books()

        case "Search User":
            admin_var.search_user()


def user():
    st.sidebar.title(f"Welcome {st.session_state.Name_of_User}")
    st.sidebar.write(f"Id # {st.session_state.id_of_user}")
    menu_for_user = st.sidebar.selectbox("Select Action",["Show Books", "Return Book" , "Borrowed Books", "Search Book"])
    
    match menu_for_user:
        case "Show Books":
            user_var.show_book(st.session_state.id_of_user)
        case "Return Book":
            user_var.return_book(st.session_state.id_of_user)
        case "Borrowed Books":
            user_var.borrowed_book(st.session_state.id_of_user)
        case "Search Book":
            user_var.search_book(st.session_state.id_of_user)


def store_userdata(cnic, name_of_user):
    if name_of_user == "":
        st.error("Invalid Credentials !!!")
        return
    if len(cnic) != 13:
        st.error("CNIC should contains 13 digit !!!")
        return

    with open("./user.json", "r") as file:
        data = json.load(file)

    for user in data:
        if user["cnic"] == cnic:
            st.error("Already has an account !!")
            return
    
    no_of_users = len(data)
    
    user_data = {
        "user_id" : no_of_users + 72591,
        "name" : name_of_user,
        "cnic" : cnic,
        "borrowed_book" : 0,
        "b_book_name" : []
    }


    data.append(user_data)

    with open("./user.json", "w") as file:
        json.dump(data, file, indent=4)

    st.session_state.is_login = True
    st.session_state.Name_of_User = name_of_user
    st.session_state.id_of_user = no_of_users + 72591
    check()
    


# --------------------------
# Check For User Or Admin
# --------------------------

def check():
    if st.session_state.is_login == False:

        st.title("WELCOME TO DIGITAL LIBRARY SYSTEM")
        st.write("This is a digital library system!!!")
        st.header("CONTINUE WITH: ")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Admin", icon=":material/manage_accounts:", use_container_width=True):
                st.session_state.admin_state = True
                st.session_state.user_state = False

        with col2:
            if st.button("User", icon=":material/person:", use_container_width=True):
                st.session_state.user_state = True
                st.session_state.admin_state = False

        # --------------------------
        # Admin login
        # --------------------------

        if st.session_state.admin_state:
            
            if "admin_proceed" not in st.session_state:
                st.session_state.admin_proceed = False

            st.header(":material/manage_accounts: Admin Log In")
            usernme = st.text_input("Enter Username")
            passwrd = st.text_input("Enter Password", type= "password")
            if st.button("Proceed", use_container_width=True, type = "primary"):
                st.session_state.admin_proceed = True

            if st.session_state.admin_proceed:
                if admin_var.USERNAME == usernme:
                    if admin_var.PASSWORD == passwrd:
                        st.session_state.is_login = True
                        check()
                    else:
                        st.error("Invalid Credentials")
                else:
                    st.error("Invalid Credentials")
                

        # --------------------------
        # User login
        # -------------------------- 

        if st.session_state.user_state:
            if st.session_state.signup or st.session_state.login == False:
                st.header(":material/person: User Sign Up")
                cnic = st.text_input("Enter CNIC")
                name_of_user = st.text_input("Enter Your Name")
                col3, col4 = st.columns(2)
                with col3:
                    if st.button("Proceed", use_container_width=True, type = "primary"):
                        store_userdata(cnic=cnic, name_of_user=name_of_user)
                with col4:
                    if st.button("Log In", use_container_width=True):
                        st.session_state.login = True
                        st.session_state.signup = False

            elif st.session_state.login or st.session_state.signup == False:
                st.header(":material/person: User Log In")
                cnic = st.text_input("Enter CNIC")
                name_of_user = st.text_input("Enter Your Name")
                id = st.text_input("Enter User Id")
                col5, col6 = st.columns(2)
                with col5:
                    if st.button("Proceed", use_container_width=True, type = "primary"):
                        with open("./user.json", "r") as file:
                            data = json.load(file)
                        for user in data:
                            if str(user["user_id"]) == id:
                                if user["cnic"] == cnic:
                                    if user["name"] == name_of_user:
                                        st.session_state.Name_of_User = name_of_user
                                        st.session_state.id_of_user = user["user_id"]
                                        st.session_state.is_login = True
                                        break
                        else:
                            st.error("Invalid Credentials")
                        
                with col6:
                    if st.button("Sign Up", use_container_width=True):
                        st.session_state.login = False
                        st.session_state.signup = True
                        

if st.session_state.is_login == False:
    check()

else:

    if st.session_state.admin_state:
        admin()
        
    else:
        user()



