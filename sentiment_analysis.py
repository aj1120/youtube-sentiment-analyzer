import mysql.connector
from textblob import TextBlob

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Strong@123",
    database="project"
)
cursor = conn.cursor()

# Fetch rows where Sentiment_score is NULL (to reprocess)
cursor.execute("SELECT id, comment_text FROM youtube_comments WHERE Sentiment_score IS NULL")
rows = cursor.fetchall()

print(f"🧠 Processing {len(rows)} comments...")

for comment_id, text in rows:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to +1
    sentiment_score_percent = round((polarity + 1) * 50, 2)  # Convert to 0–100 scale

    label = (
        "positive" if polarity > 0 else
        "negative" if polarity < 0 else
        "neutral"
    )

    print(f"📝 Comment ID: {comment_id} | Score: {sentiment_score_percent}% | Label: {label}")

    # Update sentiment label and score
    cursor.execute(
        "UPDATE youtube_comments SET Sentiment_Analysis = %s, Sentiment_score = %s WHERE id = %s",
        (label, sentiment_score_percent, comment_id)
    )

conn.commit()
cursor.close()
conn.close()

print("✅ Sentiment analysis complete and scores updated.")
