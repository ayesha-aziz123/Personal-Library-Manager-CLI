import os
import sqlite3
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Database file
DATABASE_FILE = "library.db"

# Initialize the database and create table if not exists
def initialize_database():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  author TEXT NOT NULL,
                  year INTEGER NOT NULL,
                  genre TEXT NOT NULL,
                  read_status INTEGER NOT NULL)''')
    conn.commit()
    conn.close()


# Add a book to the library
def add_book():
    print(Fore.CYAN + "\n📖 Add a Book")
    title = input("📌 " + Fore.YELLOW + "Enter the book title: " + Fore.RESET)
    author = input("✍️ " + Fore.YELLOW + "Enter the author's name: " + Fore.RESET)
    year = input("📅 " + Fore.YELLOW + "Enter the publication year: " + Fore.RESET)
    genre = input("📚 " + Fore.YELLOW + "Enter the genre: " + Fore.RESET)
    read_status = input("📖 " + Fore.YELLOW + "Have you read this book? (Yes/No): " + Fore.RESET).strip().lower() == "yes"
    
    if title and author and genre and year.isdigit():
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO books (title, author, year, genre, read_status) VALUES (?, ?, ?, ?, ?)",
                  (title, author, int(year), genre, read_status))
        conn.commit()
        conn.close()
        print(Fore.GREEN + "✅ Book added successfully!")
    else:
        print(Fore.RED + "❌ Please fill in all fields correctly.")


# Remove a book from the library by title
def remove_book():
    print(Fore.RED + "\n❌ Remove a Book")
    title = input("🔍 " + Fore.YELLOW + "Enter the title of the book to remove: " + Fore.RESET)
    
    if title:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE title = ?", (title,))
        conn.commit()
        conn.close()
        print(Fore.GREEN + f"✅ '{title}' removed successfully!")
    else:
        print(Fore.RED + "❌ Please enter a title.")


# Search for a book by title or author
def search_book():
    print(Fore.YELLOW + "\n🔍 Search for a Book")
    search_by = input(Fore.CYAN + "Search by (Title/Author): ").strip().lower()
    search_term = input(Fore.CYAN + f"Enter the {search_by}: ").strip().lower()
    
    if search_term:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        if search_by == "title":
            c.execute("SELECT * FROM books WHERE LOWER(title) LIKE ?", ('%' + search_term + '%',))
        elif search_by == "author":
            c.execute("SELECT * FROM books WHERE LOWER(author) LIKE ?", ('%' + search_term + '%',))
        matching_books = c.fetchall()
        conn.close()
        
        if matching_books:
            print(Fore.GREEN + "📚 Matching Books:")
            for i, book in enumerate(matching_books, start=1):
                status = Fore.GREEN + "✅ Read" if book[5] else Fore.RED + "❌ Unread"
                print(f"{Fore.BLUE}{i}. {Fore.YELLOW}{book[1]} {Fore.WHITE}by {book[2]} ({book[3]}) - {book[4]} - {status}")
        else:
            print(Fore.RED + "❌ No matching books found.")
    else:
        print(Fore.RED + "❌ Please enter a search term.")


# Display all books in the library
def display_all_books():
    print(Fore.BLUE + "\n📚 Your Library")
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()
    
    if not books:
        print(Fore.RED + "🚫 No books in the library.")
        return
    
    for i, book in enumerate(books, start=1):
        status = Fore.GREEN + "✅ Read" if book[5] else Fore.RED + "❌ Unread"
        print(f"{Fore.MAGENTA}{i}. {Fore.YELLOW}{book[1]} {Fore.WHITE}by {book[2]} ({book[3]}) - {book[4]} - {status}")


# Display library statistics
def display_statistics():
    print(Fore.BLUE + "\n📊 Library Statistics")
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM books")
    total_books = c.fetchone()[0]
    
    if total_books == 0:
        print(Fore.RED + "🚫 No books in the library.")
        return
    
    c.execute("SELECT COUNT(*) FROM books WHERE read_status = 1")
    read_books = c.fetchone()[0]
    percentage_read = (read_books / total_books) * 100
    
    print(Fore.YELLOW + f"📖 **Total books:** {Fore.GREEN}{total_books}")
    print(Fore.CYAN + f"📈 **Percentage read:** {Fore.GREEN}{percentage_read:.1f}%")
    conn.close()


# Main Menu
def main():
    print(Fore.BLUE + "📚 Personal Library Manager")
    print(Fore.CYAN + "Welcome to your personal library! Manage your book collection with ease.")
    
    # Initialize database at startup
    initialize_database()
    
    while True:
        print(Fore.MAGENTA + "\n📜 Menu:")
        print(Fore.YELLOW + "1️⃣  Add a Book")
        print(Fore.YELLOW + "2️⃣  Remove a Book")
        print(Fore.YELLOW + "3️⃣  Search for a Book")
        print(Fore.YELLOW + "4️⃣  Display All Books")
        print(Fore.YELLOW + "5️⃣  Display Statistics")
        print(Fore.RED + "6️⃣  Exit")
        
        choice = input(Fore.CYAN + "🎯 Choose an option (1-6): ").strip()
        
        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            search_book()
        elif choice == "4":
            display_all_books()
        elif choice == "5":
            display_statistics()
        elif choice == "6":
            print(Fore.RED + "👋 Goodbye! Happy Reading! 📖")
            break
        else:
            print(Fore.RED + "❌ Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
