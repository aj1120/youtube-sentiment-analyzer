
from googleapiclient.discovery import build
import mysql.connector
import json
from datetime import datetime
import time

# YouTube API Key and Video ID
YOUTUBE_API_KEY = 'AIzaSyCFLzyjEzBfUhG6f9p5fVLvcgSLXyL7gcc'  # Replace with your actual YouTube API key
VIDEO_ID = 'dQw4w9WgXcQ'  # Replace with the YouTube video ID you want to scrape
MYSQL_HOST = 'localhost'  # Change if MySQL is hosted elsewhere
MYSQL_USER = 'root'  # MySQL username
MYSQL_PASSWORD = 'Strong@123'  # MySQL password
MYSQL_DB = 'project'  # Your MySQL database

# Set up YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Connect to MySQL database
conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB
)
cursor = conn.cursor()

# Function to fetch comments from YouTube
def fetch_comments(video_id, max_comments=100):
    comments = []
    next_page_token = None
    while len(comments) < max_comments:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token,
            textFormat="plainText"
        ).execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'text': comment['textDisplay'],
                'author': comment['authorDisplayName'],
                'published_at': comment['publishedAt']
            })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return comments

# Insert comments into MySQL database
def insert_comments_to_mysql(comments):
    for comment in comments:
        comment_id = comment['author'] + "_" + str(datetime.now().timestamp())  # Example unique id
        text = comment['text']
        author = comment['author']
        published_at = datetime.fromisoformat(comment['published_at'].replace("Z", "+00:00"))  # Convert ISO string to datetime

        try:
            cursor.execute("""
                INSERT INTO youtube_comments (id, comment_text, author, comment_timestamp)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE comment_text = VALUES(comment_text), comment_timestamp = VALUES(comment_timestamp);
            """, (comment_id, text, author, published_at))
            conn.commit()
            print(f"Inserted comment by {author}: {text[:30]}...")  # Print first 30 characters of comment
        except mysql.connector.Error as err:
            print(f"Error inserting comment: {err}")

# Main loop to fetch and insert comments periodically
try:
    while True:
        print("Fetching new comments...")
        comments = fetch_comments(VIDEO_ID)
        if comments:
            insert_comments_to_mysql(comments)
            print(f"Inserted {len(comments)} comments into MySQL")
        time.sleep(60)  # Wait 60 seconds before fetching again
except KeyboardInterrupt:
    print("🛑 Stopping producer...")

finally:
    cursor.close()
    conn.close() 


























### This code is **scrap data/producer**

''' from googleapiclient.discovery import build
from kafka import KafkaProducer
import json
import time

YOUTUBE_API_KEY = 'AIzaSyCFLzyjEzBfUhG6f9p5fVLvcgSLXyL7gcc'
VIDEO_ID = 'dQw4w9WgXcQ'
KAFKA_TOPIC = 'youtube_comments'

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_comments(video_id, max_comments=100):
    comments = []
    next_page_token = None
    while len(comments) < max_comments:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token,
            textFormat="plainText"
        ).execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'text': comment['textDisplay'],
                'author': comment['authorDisplayName'],
                'published_at': comment['publishedAt']
            })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return comments

if __name__ == '__main__':
    while True:
        comments = fetch_comments(VIDEO_ID)
        for comment in comments:
            producer.send(KAFKA_TOPIC, comment)
        print(f"Pushed {len(comments)} comments to Kafka")
        time.sleep(60)


try:
    while True:
        comments = fetch_comments(VIDEO_ID)
        for comment in comments:
            producer.send(KAFKA_TOPIC, comment)
        print(f"Pushed {len(comments)} comments to Kafka")
        time.sleep(60)
except KeyboardInterrupt:
    print("🛑 Stopping producer...")
    producer.close() '''
