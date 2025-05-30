from confluent_kafka import Consumer, KafkaException
import mysql.connector
import json
from datetime import datetime

# MySQL Connection Parameters
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Strong@123'
MYSQL_DB = 'project'

# Connect to MySQL database
conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB
)
cursor = conn.cursor()

# Configure Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'comment_consumer_group',
    'auto.offset.reset': 'earliest'
})

# Subscribe to the Kafka topic
consumer.subscribe(['youtube_comments'])

# Insert comments into MySQL database
def insert_comments_to_mysql(youtube_comments):
    for comment in youtube_comments:
        comment_id = comment['author'] + "_" + str(datetime.now().timestamp())
        text = comment['text']
        author = comment['author']
        published_at = datetime.fromisoformat(comment['published_at'].replace("Z", "+00:00"))

        try:
            cursor.execute("""
                INSERT INTO youtube_comments (id, comment_text, author, comment_timestamp)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE comment_text = VALUES(comment_text), comment_timestamp = VALUES(comment_timestamp);
            """, (comment_id, text, author, published_at))
            conn.commit()
            print(f"Inserted comment by {author}: {text[:30]}...")
        except mysql.connector.Error as err:
            print(f"Error inserting comment: {err}")

# Consumer functionality
def run_consumer():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            comment = json.loads(msg.value().decode('utf-8'))
            insert_comments_to_mysql([comment])
    except KeyboardInterrupt:
        print("Consumer interrupted.")
    finally:
        consumer.close()
        conn.close()

if __name__ == "__main__":
    run_consumer()






