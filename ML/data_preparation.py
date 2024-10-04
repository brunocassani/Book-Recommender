import sqlite3
import pandas as pd
import re

# Connect to the SQLite database
def load_data_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Fetch all comments
    cursor.execute("SELECT rowid, body FROM comments")
    rows = cursor.fetchall()

    comments_df = pd.DataFrame(rows, columns=["id", "body"])
    conn.close()

    return comments_df

# Clean text by removing emojis/other cleaning steps
def clean_text(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)

    text = emoji_pattern.sub(r'', text)  # Remove emojis
    text = text.lower().strip()  # Convert to lowercase and strip extra spaces
    return text

# Prepare dataset with cleaned data and labels
def prepare_dataset(comments_df):
    # Add a column for cleaned text
    comments_df['cleaned_body'] = comments_df['body'].apply(clean_text)

    # Add a column for labels (1 if it contains a book title, 0 otherwise) 
    # (manually labeled a few for initial testing)
    comments_df['label'] = 0  # For now, all are labeled as 0

    return comments_df

# Save cleaned dataset to CSV for use in training
def save_cleaned_dataset(df, output_file):
    df.to_csv(output_file, index=False)

# Main function to run the preparation steps
if __name__ == "__main__":
    db_path = "book_suggestions.db"
    output_file = "cleaned_comments.csv"

    # Load, clean, and prepare the dataset
    comments_df = load_data_from_db(db_path)
    comments_df = prepare_dataset(comments_df)
    
    # Save the cleaned dataset
    save_cleaned_dataset(comments_df, output_file)

    print(f"Data saved to {output_file}. Ready for training.")

