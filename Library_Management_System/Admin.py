import streamlit as st
import json

class Admin:
    USERNAME = "admin"
    PASSWORD = "admin"

    def show_books(self):
        
        with open("./data.json", "r") as file:
            books = json.load(file)

        for book in books:
            st.header(book["title"])
            col1, col2 = st.columns(2)
            with col1:
                st.write("Author : " + book["author"])
            
            with col2:
                st.write("Book ID : " + str(book["id"]))
            
            col3, col4 = st.columns(2)
            with col3:
                st.write("Total Copies : " + str(book["no_of_copies"]))
            
            with col4:
                st.write("Available Copies : " + str(book["available_copies"]))
            st.write("--------------------------------")

    def add_book(self):

        title = ""
        author = ""
        copies = 0

        choice = st.sidebar.radio(" **Select :** ", ["Add Existing Book", "Add New Book"])

        if choice == "Add New Book":
            st.title("ADD NEW BOOK")

            title = st.text_input("Enter Title Of Book")
            author = st.text_input("Enter Author Of Book")
            copies = st.number_input("Enter No. of Copies", min_value=0, step=1)

            if st.button("Add Book", use_container_width=True, type = "primary"):

                with open("./data.json", "r") as file:
                    books = json.load(file)

                book_id = len(books) + 62851

                data = {
                    "id" : book_id,
                    "title" : title,
                    "author" : author,
                    "no_of_copies" : copies,
                    "available_copies" : copies
                }

                books.append(data)

                st.success("Succcessfully Added !!!")

                with open("./data.json", "w") as file:
                    json.dump(books, file, indent=4)
        
        elif choice == "Add Existing Book":
            st.title("ADD EXISTING BOOK")

            title = st.text_input("Enter Title Of Book")
            author = st.text_input("Enter Author Of Book")
            Id = st.text_input("Enter Book ID")
            copies_to_remove = st.number_input("Enter No. of Copies to Add", min_value=0, step=1)

            if st.button("Add Book", use_container_width=True, type = "primary"):

                with open("./data.json", "r") as file:
                    books = json.load(file)

                for book in books:
                    if book["title"] == title:
                        if book["author"] == author:
                            if book["id"] == int(Id):
                                
                                book["available_copies"] = book["available_copies"] + copies_to_remove
                                book["no_of_copies"] = book["no_of_copies"] + copies_to_remove
                                st.success("Successfully Added !!!")

                                with open("./data.json", "w") as file:
                                    json.dump(books, file, indent=4)

                                break

                                
                                
                else:
                    st.error("No Book Available !!!")


    def remove_book(self):
        
        st.title("REMOVE BOOK")

        title = st.text_input("Enter Title Of Book")
        author = st.text_input("Enter Author Of Book")
        Id = st.text_input("Enter Book ID")
        copies_to_remove = st.number_input("Enter No. of Copies to Remove", min_value=0, step=1)

        if st.button("Remove Book", use_container_width=True, type = "primary"):

            with open("./data.json", "r") as file:
                books = json.load(file)

            new_list = []

            def remove(id):
                for book in books:                  
                    if book["id"] != id:
                        new_list.append(book)

            for book in books:
                if book["title"] == title:
                    if book["author"] == author:
                        if book["id"] == int(Id):
                            if book["available_copies"] < copies_to_remove and book["no_of_copies"] >= copies_to_remove:
                                st.error("Book are not available for removal!!!")
                                break
                            elif book["no_of_copies"] < copies_to_remove:
                                st.error(f"Not Enough Books To Remove!!! , You have total {book["no_of_copies"]} copies")
                                break
                            elif book["available_copies"]==book["no_of_copies"] and book["no_of_copies"] == copies_to_remove:
                                remove(book["id"])
                                with open("./data.json", "w") as file:
                                    json.dump(new_list, file, indent=4)
                                st.success("Successfully Removed!!!")
                                break
                            elif book["available_copies"] >= copies_to_remove :
                                book["available_copies"] = book["available_copies"] - copies_to_remove
                                book["no_of_copies"] = book["no_of_copies"] - copies_to_remove
                                st.success("Successfully Removed!!!")

                                with open("./data.json", "w") as file:
                                    json.dump(books, file, indent=4)

                                break

                        
            else:
                st.error("No Book Available !!!")

    def borrowed_books(self):
        
        with open("./data.json", "r") as file:
            books = json.load(file)

        for book in books:
            if book["no_of_copies"] > book["available_copies"]:

                with open("./user.json", "r") as files:
                    users = json.load(files)

                borrowed_book_user = []

                for user in users:
                    for title in user["b_book_name"]:
                        if title[0] == book["title"]:
                            if title[1] == book["author"]:
                                borrowed_book_user.append([user["user_id"], title[2]])                              

                st.header(book["title"])
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Author : " + book["author"])
                
                with col2:
                    st.write("Book ID : " + str(book["id"]))
                
                col3, col4 = st.columns(2)
                with col3:
                    st.write("Total Copies : " + str(book["no_of_copies"]))
                
                with col4:
                    st.write("Available Copies : " + str(book["available_copies"]))

                st.subheader("Users Data: ")

                col5, col6 = st.columns(2)
                i = 1
                for data in borrowed_book_user:
                    i += 1
                    with col5:
                        if (i%2 == 0):
                            st.write(" - User Id : " + str(data[0]) + " &nbsp; || &nbsp; No. of copies : " + str(data[1]))
                    
                    with col6:
                        if (i%2 == 1):
                            st.write(" - User Id : " + str(data[0]) + " &nbsp; || &nbsp; No. of copies : " + str(data[1]))
                st.divider()

    def search_books(self):

        st.sidebar.write("")
        role = st.sidebar.radio("**Search By :** ", ["Search By Title", "Search By Author", "Search By Id"])

        with open("./data.json", "r") as file:
            books = json.load(file)

        match role:
            case "Search By Title":

                if "title_search" not in st.session_state:
                    st.session_state.title_search = False

                st.title("Search By Title")
                title = st.text_input("Enter Title")
                if st.button("Search", use_container_width=True, type = "primary"):
                    st.session_state.title_search = True
                
                if st.session_state.title_search:
                    for book in books:                
                        if title == book["title"]:
                            
                            st.divider()
                            st.header(book["title"])
                            col1, col2 = st.columns(2)

                            with col1:
                                st.write("Author : " + book["author"])

                            with col2:
                                st.write("Book ID : " + str(book["id"]))

                            col3, col4, col5 = st.columns([2,1,1])

                            with col3:
                                st.write("Total Copies : " + str(book["no_of_copies"]))

                            with col4:
                                st.write("Available Copies : " + str(book["available_copies"]))
                            st.session_state.title_search = False
                            break
                    else:
                        st.error("No Book Available !!!")
                        st.session_state.title_search = False



            case "Search By Author":

                if "author_search" not in st.session_state:
                    st.session_state.author_search = False

                st.title("Search By Author")
                author = st.text_input("Enter Author Name")
                if st.button("Search", use_container_width=True, type = "primary"):
                    st.session_state.author_search = True
                
                if st.session_state.author_search:
                    for book in books:                
                        if author == book["author"]:
                            
                            st.divider()
                            st.header(book["title"])
                            col1, col2 = st.columns(2)

                            with col1:
                                st.write("Author : " + book["author"])

                            with col2:
                                st.write("Book ID : " + str(book["id"]))

                            col3, col4, col5 = st.columns([2,1,1])

                            with col3:
                                st.write("Total Copies : " + str(book["no_of_copies"]))

                            with col4:
                                st.write("Available Copies : " + str(book["available_copies"]))
                            st.session_state.author_search = False
                            break
                    else:
                        st.error("No Book Available !!!")
                        st.session_state.author_search = False

            case "Search By Id":

                if "id_search" not in st.session_state:
                    st.session_state.id_search = False

                st.title("Search By Id")
                id_by_user = st.text_input("Enter Book Id")
                if st.button("Search", use_container_width=True, type = "primary"):
                    st.session_state.id_search = True
                
                if st.session_state.id_search:
                    for book in books:                
                        if id_by_user == str(book["id"]):
                            
                            st.divider()
                            st.header(book["title"])
                            col1, col2 = st.columns(2)

                            with col1:
                                st.write("Author : " + book["author"])

                            with col2:
                                st.write("Book ID : " + str(book["id"]))

                            col3, col4, col5 = st.columns([2,1,1])

                            with col3:
                                st.write("Total Copies : " + str(book["no_of_copies"]))

                            with col4:
                                st.write("Available Copies : " + str(book["available_copies"]))
                            st.session_state.id_search = False
                            break
                    else:
                        st.error("No Book Available !!!")
                        st.session_state.id_search = False

    def search_user(self):

        st.sidebar.write("")
        role = st.sidebar.radio("**Search By :** ", ["Search By Name", "Search By Id", "Search By CNIC"])

        with open("./user.json", "r") as file:
            users = json.load(file)

        match role:
            case "Search By Name":

                if "name_search" not in st.session_state:
                    st.session_state.name_search = False

                st.title("Search By Name")
                name = st.text_input("Enter Name")
                if st.button("Search", use_container_width=True, type = "primary"):
                    st.session_state.name_search = True
                
                if st.session_state.name_search:
                    for user in users:                
                        if name == user["name"]:
                            
                            st.divider()
                            st.title(user["name"])
                            col1, col2 = st.columns(2)

                            with col1:
                                st.subheader("CNIC : " + user["cnic"])

                            with col2:
                                st.subheader("User ID : " + str(user["user_id"]))

                            for book_b_list in user["b_book_name"]:
                                st.divider()
                                st.subheader(book_b_list[0])
                                col3, col4 = st.columns(2)
                                with col3:
                                    st.write("Author : " + book_b_list[1])

                                with col4:
                                    st.write("No. of Copies : " + str(book_b_list[2]))
                            
                            break
                    
                    else:
                        st.error("No User Found !!!")
                    
                    st.session_state.name_search = False
                        
                    




            case "Search By Id":

                if "id_b_search" not in st.session_state:
                    st.session_state.id_b_search = False

                st.title("Search By Id")
                id_user = st.text_input("Enter Id")
                if st.button("Search", use_container_width=True, type = "primary"):
                    st.session_state.id_b_search = True
                
                if st.session_state.id_b_search:
                    for user in users:                
                        if id_user == str(user["user_id"]):
                            
                            st.divider()
                            st.title(user["name"])
                            col1, col2 = st.columns(2)

                            with col1:
                                st.subheader("CNIC : " + user["cnic"])

                            with col2:
                                st.subheader("User ID : " + str(user["user_id"]))

                            for book_b_list in user["b_book_name"]:
                                st.divider()
                                st.subheader(book_b_list[0])
                                col3, col4 = st.columns(2)
                                with col3:
                                    st.write("Author : " + book_b_list[1])

                                with col4:
                                    st.write("No. of Copies : " + str(book_b_list[2]))
                            
                            break
                    
                    else:
                        st.error("No User Found !!!")
                    
                    st.session_state.id_b_search = False

            case "Search By CNIC":

                if "cnic_search" not in st.session_state:
                    st.session_state.cnic_search = False

                st.title("Search By CNIC")
                cnic = st.text_input("Enter CNIC")
                if st.button("Search", use_container_width=True, type = "primary"):
                    if len(cnic) == 13:
                        st.session_state.cnic_search = True
                    else:
                        st.error("CNIC Should have 13 digits !!! ")
                
                if st.session_state.cnic_search:
                    for user in users:                
                        if cnic == user["cnic"]:
                            
                            st.divider()
                            st.title(user["name"])
                            col1, col2 = st.columns(2)

                            with col1:
                                st.subheader("CNIC : " + user["cnic"])

                            with col2:
                                st.subheader("User ID : " + str(user["user_id"]))

                            for book_b_list in user["b_book_name"]:
                                st.divider()
                                st.subheader(book_b_list[0])
                                col3, col4 = st.columns(2)
                                with col3:
                                    st.write("Author : " + book_b_list[1])

                                with col4:
                                    st.write("No. of Copies : " + str(book_b_list[2]))
                            
                            break
                    
                    else:
                        st.error("No User Found !!!")  

                    st.session_state.cnic_search = False  

                



            


        
                                


            


            


        

