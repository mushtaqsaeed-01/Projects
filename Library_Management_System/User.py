import streamlit as st
import json

class User:
    def show_book(self, id):
        with open("./data.json", "r") as file:
            books = json.load(file)

        with open("./user.json", "r") as files:
            users = json.load(files)

        if "is_success" not in st.session_state:
            st.session_state.is_success = False

        for book in books:
            if book["available_copies"] > 0:
                st.header(book["title"])
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Author : " + book["author"])
    
                with col2:
                    st.write("Book ID : " + str(book["id"]))
    
                col3, col4, col5 = st.columns([2,1,1])
                with col3:
                    st.write("Available Copies : " + str(book["available_copies"]))
    
    
                with col4:
                    if st.button("Borrow", key= f"{book["title"]}_borrow", use_container_width=True, type = "primary"):                                 
                        book["available_copies"] = book["available_copies"] - 1
                        for user in users:
                            if user["user_id"] == id:
                                user["borrowed_book"] = user["borrowed_book"] + 1
                                for book_list in user["b_book_name"]:
                                    if book_list[0] == book["title"]:
                                        book_list[2] = book_list[2] + 1
                                        st.session_state.is_success = True 
                                        break
                                else:
                                    user["b_book_name"].append([book["title"], book["author"], 1])
                                    st.session_state.is_success = True
    
                if st.session_state.is_success:
                    st.success("Borrowed Successfully !!!")
                    st.session_state.is_success = False             
                st.write("--------------------------------")
        
        with open("./user.json", "w") as update:
            json.dump(users, update, indent=4)
        with open("./data.json", "w") as update_data:
            json.dump(books, update_data, indent=4)

    def return_book(self, id):

        st.title("RETURN BOOK")

        title = st.text_input("Enter Title Of Book")
        author = st.text_input("Enter Author Of Book")
        copies_to_remove = st.number_input("Enter No. of Copies to Return", min_value=0, step=1)

        if st.button("Return", use_container_width=True, type = "primary"):

            with open("./data.json", "r") as file:
                books = json.load(file)

            with open("./user.json", "r") as files:
                users = json.load(files)

            new_list = []

            def remove_book_u(title, id):
                for user in users:
                    if user["user_id"] != id:
                        new_list.append(user)
                    else:
                        booksList = []
                        for book_list in user["b_book_name"]:
                            if book_list[0] != title:
                                booksList.append(book_list)
                        user["b_book_name"] = booksList
                        new_list.append(user)

            def add_book_u(title, author, no_of_copy):
                for book in books:
                    if book["title"] == title:
                        if book["author"] == author:
                            book["available_copies"] = book["available_copies"] + no_of_copy

            for user in users:
                if user["user_id"] == id:
                    for book_list in user["b_book_name"]:
                        if book_list[0] == title:
                            if book_list[1] == author:
                                if book_list[2] > copies_to_remove:
                                    book_list[2] = book_list[2] - copies_to_remove
                                    add_book_u(title=title, author=author, no_of_copy=copies_to_remove)
                                    user["borrowed_book"] = user["borrowed_book"] - copies_to_remove
                                    with open("./user.json", "w") as file:
                                        json.dump(users, file, indent=4)
                                    st.success("Successfully Returned !!!")
                                    break
                                    

                                elif book_list[2] < copies_to_remove:
                                    st.error("Not Enough Copies To Return!!!")
                                    break
                                else:
                                    user["borrowed_book"] = user["borrowed_book"] - copies_to_remove
                                    remove_book_u(title=title, id=id)
                                    add_book_u(title=title, author=author, no_of_copy=copies_to_remove)
                                    with open("./user.json", "w") as file:
                                        json.dump(new_list, file, indent=4)
                                    with open("./data.json", "w") as file:
                                        json.dump(books, file, indent=4)
                                    st.success("Successfully Returned !!!")
                                    break
                                    

                    else:
                        st.error("Book Not Found !!!")
    
    def borrowed_book(self, id):

        with open("./user.json", "r") as files:
            users = json.load(files)

        with open("./data.json", "r") as file:
            books = json.load(file)
        
        for user in users:
            if user["user_id"] == id:
                st.header("Total Number Of Books: " + str(user["borrowed_book"]))
                for book_list in user["b_book_name"]:
                    bookId = 0
                    for book in books:
                        if book["title"] == book_list[0]:
                            if book["author"] == book_list[1]:
                                bookId = book["id"]

                    st.write("---------------------------------")
                    st.header(book_list[0])
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("Author : " + book_list[1])

                    with col2:
                        st.write("Book ID : " + str(bookId))

                    st.write("Available Copies : " + str(book_list[2]))
    
    def search_book(self, id):

        if "is_book_found" not in st.session_state:
            st.session_state.is_book_found = False

        st.sidebar.write("")
        role = st.sidebar.radio("**Search By :** ", ["Search By Title", "Search By Author", "Search By Id"])

        with open("./data.json", "r") as file:
            books = json.load(file)

        with open("./user.json", "r") as files:
            users = json.load(files)

        match role:
            case "Search By Title":

                if "title_search" not in st.session_state:
                    st.session_state.title_search = False

                st.title("Search By Title")
                title = st.text_input("Enter Title")
                if st.button("Search", use_container_width=True, type = "primary"):
                    st.session_state.title_search = True
                
                if st.session_state.title_search:
                    st.session_state.is_book_found = False
                    for book in books:                
                        if title == book["title"]:
                            st.session_state.is_book_found = True
                            if "is_success" not in st.session_state:
                                st.session_state.is_success = False
                            
                            st.divider()
                            st.header(book["title"])
                            col1, col2 = st.columns(2)

                            with col1:
                                st.write("Author : " + book["author"])

                            with col2:
                                st.write("Book ID : " + str(book["id"]))

                            col3, col4, col5 = st.columns([2,1,1])

                            with col3:
                                st.write("Available Copies : " + str(book["available_copies"]))

                            with col4:
                                if st.button("Borrow", use_container_width=True, type = "primary"):              
                                    if book["available_copies"] > 0:
                                        book["available_copies"] = book["available_copies"] - 1
                                        for user in users:
                                            if user["user_id"] == id:
                                                user["borrowed_book"] = user["borrowed_book"] + 1
                                                for book_list in user["b_book_name"]:
                                                    if book_list[0] == book["title"]:
                                                        book_list[2] = book_list[2] + 1
                                                        st.session_state.is_success = True
                                                        break
                                                else:
                                                    user["b_book_name"].append([book["title"], book["author"], 1])
                                                    st.session_state.is_success= True
                                    else:
                                        st.error("Book Not Available for Borrowing")

                            if st.session_state.is_success:
                                st.success("Borrowed Successfully !!!")
                                st.session_state.is_success = False
                                st.session_state.title_search = False
                            

                    if st.session_state.is_book_found == False:
                        st.error("Book Not Found !!!")
                        st.session_state.is_book_found = False
                        st.session_state.title_search = False


            case "Search By Author":

                if "author_search" not in st.session_state:
                    st.session_state.author_search = False

                st.title("Search By Author")
                author = st.text_input("Enter Author Name")
                if st.button("Search", use_container_width=True, type = "primary"):
                    st.session_state.author_search = True
                
                if st.session_state.author_search:
                    st.session_state.is_book_found = False
                    for book in books:                
                        if author == book["author"]:

                            st.session_state.is_book_found = True
                            if "is_success" not in st.session_state:
                                st.session_state.is_success = False
                            
                            st.divider()
                            st.header(book["title"])
                            col1, col2 = st.columns(2)

                            with col1:
                                st.write("Author : " + book["author"])

                            with col2:
                                st.write("Book ID : " + str(book["id"]))

                            col3, col4, col5 = st.columns([2,1,1])

                            with col3:
                                st.write("Available Copies : " + str(book["available_copies"]))

                            with col4:
                                if st.button("Borrow", use_container_width=True, type = "primary"):              
                                    if book["available_copies"] > 0:
                                        book["available_copies"] = book["available_copies"] - 1
                                        for user in users:
                                            if user["user_id"] == id:
                                                user["borrowed_book"] = user["borrowed_book"] + 1
                                                for book_list in user["b_book_name"]:
                                                    if book_list[0] == book["title"]:
                                                        book_list[2] = book_list[2] + 1
                                                        st.session_state.is_success = True
                                                        break
                                                else:
                                                    user["b_book_name"].append([book["title"], book["author"], 1])
                                                    st.session_state.is_success= True
                                    else:
                                        st.error("Book Not Available for Borrowing")

                            if st.session_state.is_success:
                                st.success("Borrowed Successfully !!!")
                                st.session_state.is_success = False
                                st.session_state.author_search = False

                    if st.session_state.is_book_found == False:
                        st.error("Book Not Found !!!")
                        st.session_state.is_book_found = False
                        st.session_state.author_search = False

            case "Search By Id":

                if "id_search" not in st.session_state:
                    st.session_state.id_search = False

                st.title("Search By Id")
                id_by_user = st.text_input("Enter Book Id")
                if st.button("Search", use_container_width=True, type = "primary"):
                    st.session_state.id_search = True
                
                if st.session_state.id_search:
                    st.session_state.is_book_found = False
                    for book in books:                
                        if id_by_user == str(book["id"]):

                            st.session_state.is_book_found = True

                            if "is_success" not in st.session_state:
                                st.session_state.is_success = False
                            
                            st.divider()
                            st.header(book["title"])
                            col1, col2 = st.columns(2)

                            with col1:
                                st.write("Author : " + book["author"])

                            with col2:
                                st.write("Book ID : " + str(book["id"]))

                            col3, col4, col5 = st.columns([2,1,1])

                            with col3:
                                st.write("Available Copies : " + str(book["available_copies"]))

                            with col4:
                                if st.button("Borrow", use_container_width=True, type = "primary"):              
                                    if book["available_copies"] > 0:
                                        book["available_copies"] = book["available_copies"] - 1
                                        for user in users:
                                            if user["user_id"] == id:
                                                user["borrowed_book"] = user["borrowed_book"] + 1
                                                for book_list in user["b_book_name"]:
                                                    if book_list[0] == book["title"]:
                                                        book_list[2] = book_list[2] + 1
                                                        st.session_state.is_success = True
                                                        break
                                                else:
                                                    user["b_book_name"].append([book["title"], book["author"], 1])
                                                    st.session_state.is_success= True
                                    else:
                                        st.error("Book Not Available for Borrowing")

                            if st.session_state.is_success:
                                st.success("Borrowed Successfully !!!")
                                st.session_state.is_success = False
                                st.session_state.id_search = False

                    if st.session_state.is_book_found == False:
                        st.error("Book Not Found !!!")
                        st.session_state.is_book_found = False
                        st.session_state.id_search = False

        with open("./user.json", "w") as update:
            json.dump(users, update, indent=4)
        with open("./data.json", "w") as update_data:
            json.dump(books, update_data, indent=4)