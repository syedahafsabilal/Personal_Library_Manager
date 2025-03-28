import json
import streamlit as st

st.markdown(
    """
    <style>
    .stApp{
        background-image:url("https://media.istockphoto.com/id/1044049394/photo/library-of-strahov-monastery-in-prague-czech-republic.jpg?s=2048x2048&w=is&k=20&c=yYYZTV7Ekq5LwIK4UEZbhSPj6CzvGXbU0NQLOt-hlNs=");
    background-size:cover;
    background-position:center;
    background-repeat:no-repeat;
    background-attachment:fixed;
    }
    .sub-header{
     color:white !important;
     font-size:20px !important;
     font-weight:bold !important;
    }
    </style>
    """,
       unsafe_allow_html=True
)



st.markdown('<h1 style="color:white;">Book Collection Manager</h1>', unsafe_allow_html=True)
class BookCollection :

    def __init__(self):
        self.book_list = []
        self.storage_file ="books_data.json"
        self.read_from_file()
 
 


    def delete_book(self,title):
        original_length = len(self.book_list)
        self.book_list = [book for book in self.book_list if book["title"].lower() != title.lower()]

        if len(self.book_list) < original_length:
           self.save_to_file()
           print("Book deleted successfully!\n")
           return True
        else:
           print("Book not found!\n")
           return False

    def read_from_file(self):
        try:
            with open(self.storage_file, "r") as file:
                self.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []

    def save_to_file(self):
        with open(self.storage_file, "w") as file:
             json.dump(self.book_list, file, indent=4)

    def search_book(self, search_text):
           search_text = search_text.lower()
           return [
              book for book in self.book_list
              if search_text in book["title"].lower()
              or search_text in book["author"].lower()
              or search_text in book["genre"].lower()
           ]

    def create_new_book(self,title,author,year,genre,is_read):
        new_book = {
             "title": title,
             "author": author,
             "publication_year": year if year else "Unknown",
             "genre": genre,
             "is_read":is_read
    }
        
        self.book_list.append(new_book)
        self.save_to_file()
        print("Book added successfully!\n")


    def show_reading_progress(self):
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book.get("is_read",False))
        completion_rate = (completed_books / total_books) * 100 if total_books > 0 else 0 
        print(f"Total books in collection: {total_books}")
        print(f"Reading Progress:{completion_rate:.2f}%")
        return total_books, completion_rate

book_manager = BookCollection()

menu = st.sidebar.selectbox("Select an option", ["Add a new book", "View all books", "Search book", "Delete book", "Reading progress"])


if menu == "Add a new book":
    st.markdown('<p class ="sub-header">Enter the title of the book</p>', unsafe_allow_html=True)
    book_title =st.text_input("",key="book_title_add")
    st.markdown('<p class ="sub-header">Enter the author of the book</p>', unsafe_allow_html=True)
    book_author = st.text_input("",key="book_author_add")
    st.markdown('<p class ="sub-header">Enter the publication year of the book</p>', unsafe_allow_html=True)
    publication_year = st.number_input("",key="publication_year_add",min_value=1000,max_value=2025,step=1)
    st.markdown('<p class ="sub-header">Enter the genre of the book</p>', unsafe_allow_html=True)
    book_genre = st.text_input("",key="book_genre_add")
    st.markdown('<p class ="sub-header">Is the book read?</p>', unsafe_allow_html=True)
    is_book_read = st.checkbox("",key="is_book_read_add")



 

    if st.button("Add book"):
      st.write(f"DEBUG: {book_title}, {book_author}, {publication_year}, {book_genre}, {is_book_read}")

      if not book_title.strip():
          st.error("Title is required")
      elif not book_author.strip():
           st.error("Author is required")
      elif not book_genre.strip():
           st.error("Genre is required")
      elif not publication_year:
           st.error("Publication year is required")
      elif publication_year < 1000 or publication_year > 2025:
           st.error("Invalid publication year")
      else:
           book_manager.create_new_book(book_title, book_author,publication_year, book_genre, is_book_read)
           st.success("Book added successfully!")


if menu =="View all books":
    books = book_manager.book_list
    if books:
        for book in books:
            reading_status = "Read" if book ["is_read"] else "Not Read"
            st.write(f"**{book['title']}** by {book['author']} ({book.get('publication_year','Unknown')} - {book['genre']} - {reading_status}")
    else:
        st.write("No books available in the collection.")


elif menu == "Search book":
    search_text = st.text_input("Enter the text to search for: ")

    if st.button("Search"):
        found_books = book_manager.search_book(search_text)

        if found_books:
           for book in found_books:
               st.write(f"**{book['title']} by {book['author']} ({book['publication_year']}) - {book['genre']}")
        else:
            st.write("No matching books found.")

elif menu == "Delete book":
    title = st.text_input("Enter the title of the book to delete: ")
    if st.button("Delete"):
       success = book_manager.delete_book(title)
       if success:
          st.success(f"Book {title} deleted successfully!")
       else:
          st.error(f"Book {title} not found.")

elif menu == "Reading progress":
    total_books, completion_rate = book_manager.show_reading_progress()
    st.write(f"Total books: {total_books}")
    st.write(f"Reading progress: {completion_rate:.2f}%")



title="Some Book title"


success = book_manager.delete_book(title)
print(f"Book deletion result: {success}")
