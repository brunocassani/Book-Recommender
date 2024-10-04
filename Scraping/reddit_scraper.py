import praw
import sqlite3
import time

# Reddit API setup (replace with your actual credentials if you're forking)
reddit = praw.Reddit(
    client_id='private, can\'t tell ya',
    client_secret='nope, not telling',
    user_agent='book_recommender',
    username='NICE TRY',
    password='NOT HAPPENING'
)

# Function to scrape posts: took about ~30 mins with the comments
def scrape_posts(subreddit_name, limit=1000):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    
    # Fetch top posts from the past year
    for post in subreddit.top(time_filter='year', limit=limit):
        flair = post.link_flair_text if post.link_flair_text else 'None'
        posts.append({
            'id': post.id,
            'title': post.title,
            'score': post.score,
            'author': post.author.name if post.author else 'N/A',
            'created': post.created_utc,
            'flair': flair
        })
    
    return posts

# Function to scrape comments for a specific post
def scrape_comments(post_id):
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=0)  # Flatten comment threads
    
    comments = []
    for comment in submission.comments.list():
        comments.append({
            'comment_id': comment.id,
            'post_id': post_id,
            'body': comment.body,
            'score': comment.score,
            'author': comment.author.name if comment.author else 'N/A'
        })
    
    return comments

# Function to set up the SQLite database
def setup_database():
    conn = sqlite3.connect('book_suggestions.db')
    c = conn.cursor()
    
    # Create posts table with flair
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            title TEXT,
            score INTEGER,
            author TEXT,
            created TIMESTAMP,
            flair TEXT
        )
    ''')
    
    # Create comments table
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            comment_id TEXT PRIMARY KEY,
            post_id TEXT,
            body TEXT,
            score INTEGER,
            author TEXT,
            FOREIGN KEY(post_id) REFERENCES posts(id)
        )
    ''')
    
    conn.commit()
    return conn, c

# Function to insert scraped posts into the database
def insert_posts(conn, cursor, posts):
    for post in posts:
        cursor.execute('''
            INSERT OR IGNORE INTO posts (id, title, score, author, created, flair) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (post['id'], post['title'], post['score'], post['author'], post['created'], post['flair']))
    conn.commit()

# Function to insert scraped comments into the database
def insert_comments(conn, cursor, post_id, comments):
    for comment in comments:
        cursor.execute('''
            INSERT OR IGNORE INTO comments (comment_id, post_id, body, score, author) 
            VALUES (?, ?, ?, ?, ?)
        ''', (comment['comment_id'], post_id, comment['body'], comment['score'], comment['author']))
    conn.commit()

# Main function to scrape posts and comments, then store them in the database
def main():
    conn, cursor = setup_database()
    
    # Scrape posts from r/booksuggestions
    print("Scraping posts...")
    posts = scrape_posts('booksuggestions', limit=1000)  # Increase limit as needed
    
    # Insert posts into the database
    insert_posts(conn, cursor, posts)
    
    # Scrape comments for each post and insert them into the database
    for post in posts:
        print(f"Scraping comments for post ID: {post['id']}")
        comments = scrape_comments(post['id'])
        insert_comments(conn, cursor, post['id'], comments)
        time.sleep(2)  # Avoid hitting Reddit's API rate limit
    
    print("Scraping complete.")
    conn.close()

if __name__ == "__main__":
    main()
