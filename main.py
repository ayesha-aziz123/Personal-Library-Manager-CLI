import json

def load_books():
    try:
        with open("library.txt","r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_books(books):
    with open("library.txt","w") as file:
        json.dump(books,file,indent=4) 

books = load_books()

def add_book():
    title = input("Enter the book title:")
    author = input("Enter the author: ")
    year = int(input("Enter the publication year: "))
    genre = input("Enter the genre: ")
    read_status = input("Have you read this book? (yes/no): ").strip().lower() == "yes"
    books.append({"Title": title, "Author": author,"Year":year,"Genre":genre,"Read":read_status})
    save_books(books)
    print("Book added successfully!✅\n")
    
def remove():
    title = input("Enter the 👉(title) name of the book to remove: ")
    global books 
    books = [book for book in books if book["Title"] != title]  
    save_books(books)  
    print("Book removed successfully!✔\n")


def search_book():
    search_query = input("Enter book title or author to search: ").lower()
    results = [search_book for search_book in books if search_query in search_book["Title"] or search_query in search_book["Author"]]
    if results:
        for book in results:
            print(f"""
                  Title: {book['Title']} 
                  Author: {book['Author']}
                  Year: {book['Year']}
                  Genre: {book['Genre']}
                  Read: {'Read' if book['Read'] else 'Unread'}""")
    else:
        print("No books found.❌\n")
        
def display_books():
    if books:
        for book in books:
            print("----------------------------------------------------------------------------")
            print(f"{book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {'Read' if book['Read'] else 'Unread'}")
            print("----------------------------------------------------------------------------")

    else:
        print("No books added yet 🙅‍♂️‼.\n")


def display_statistics():
    total_books = len(books)
    read_books = len([book for book in books if book["Read"]])
    print(f"Total books: {total_books}")
    print(f"Books Read: {read_books}")
    print(f"Percentage Read: {read_books / total_books * 100:.2f}%" if total_books > 0 else "No books available to calculate statistics.\n")


        
def main():
    global books
    books = load_books()
    while True:
        print("\n\tWelcome to your Personal Library Manager!📚\n")
        print("1.➕ Add a book")
        print("2.❌Remove a book")
        print("3.🔍 Search for a book")
        print("4.📖 Display all books")
        print("5.📊 Display statistics")
        print("6.🚪 Exit")
        choice = input("👉 Enter your choice: ")
        
        if  choice == "1":
            add_book()
        elif choice == "2":
            remove()
        elif choice == "3": 
            search_book()
        elif choice == "4":
            display_books()
        elif choice == "5":
            display_statistics()
        elif choice == "6":
            save_books(books)
            print("Library saved to file. Goodbye!😊👋")
            break
    
        else:
            print("Invalid choice! Please enter a number between 1-6.\n")


if __name__ == "__main__":
    main()
    