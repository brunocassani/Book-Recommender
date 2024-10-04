import sqlite3
#import spacy
#import json
#import re

# Connect to SQLite database
db_path = "book_suggestions.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Remove comments where the score is negative or the body is "[removed]" or "[deleted]"
cursor.execute("DELETE FROM comments WHERE score < 0 OR body IN ('[removed]', '[deleted]')")
conn.commit()  # Commit the deletion

# Remove comments that are repeated (exact same "body" AND "author")
cursor.execute("DELETE FROM comments WHERE rowid NOT IN (SELECT MIN(rowid) FROM comments GROUP BY body, author)")
conn.commit()  # Commit the deletion

#print how many rows there are for readme
#cursor.execute("SELECT COUNT(*) FROM comments")
#print(cursor.fetchone()[0])

''' Interesting code I wrote (but ultimately failed due to how specific SpaCy's NER is)
# Load SpaCy's English model
nlp = spacy.load("en_core_web_sm")

# Function to extract tentative book titles
def extract_book_titles(text):
    doc = nlp(text)
    book_titles = []

    # SpaCy's WORK_OF_ART label for book titles
    for ent in doc.ents:
        if ent.label_ == "WORK_OF_ART":
            book_titles.append(ent.text)
    
    # Regex to find quoted titles
    quote_titles = re.findall(r'"([^"]+)"', text)
    book_titles.extend(quote_titles)

    return list(set(book_titles))  # Remove duplicates

# Fetch all comments from the database after cleaning
cursor.execute("SELECT rowid, body FROM comments")
rows = cursor.fetchall()

# Loop through each comment and process it
for rowid, body in rows:
    titles = extract_book_titles(body)
    
    # If titles are found, present them for manual review
    if titles:
        print(f"Comment: {body}")
        print(f"Tentative Book Titles: {titles}")
        
        # Prompt for user input (sign off, reject, defer)
        user_input = input("Sign off [1], Reject [2], Defer [3]: ")
        
        if user_input == "1":  # Sign off: Add titles to JSON column
            titles_json = json.dumps(titles)
            cursor.execute("UPDATE comments SET titles = ? WHERE rowid = ?", (titles_json, rowid))
            conn.commit()
            print(f"Titles saved for comment {rowid}.")
        
        elif user_input == "2":  # Reject: Delete comment from table
            cursor.execute("DELETE FROM comments WHERE rowid = ?", (rowid,))
            conn.commit()
            print(f"Comment {rowid} deleted.")
        
        elif user_input == "3":  # Defer: Do nothing and move to the next comment
            print(f"Deferred comment {rowid}. Moving to the next...")
        
    else:
        print(f"No tentative titles found for comment: {body}")
        print(f"Comment {rowid} skipped.\n")
'''

# Close database connection
conn.close()

