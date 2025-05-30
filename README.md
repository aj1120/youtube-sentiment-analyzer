# youtube-sentiment-analyzer
Real-time sentiment analysis of Youtube comments using Python , MySQL and GCP YouTube Data API.
Extract data with help of kafka Producer, read data with help of Consumer both of this build cordination between with help of zookeeper.


## 🔧 Technologies Used
- Python
- MySQL
- TextBlob
- YouTube Data API
- Git & GitHub
- kafka
- Zookeeper
## 📂 Features
- Fetches live comments from YouTube videos
- Analyzes sentiment (positive, negative, neutral)
- Stores data in MySQL database
- Modular and production-ready codebase

## 📁 Project Structure
- `producer.py`: Fetch comments and send to Kafka
- `consumer.py`: Process and store comments
- `sentiment_analyzer.py`: Analyze comment sentiment
- `db_schema.sql`: MySQL schema setup

## 🚀 Setup Instructions
1. Clone this repo
2. Install requirements: `pip install -r requirements.txt`
3. Setup MySQL and run `db_schema.sql`
4. Run `producer.py` and `consumer.py`

## 📸 Sample Output
![Sample Screenshot](sample_output/results.png)

## 🧠 Future Improvements
- Add a web dashboard (Flask/Django)
- Use machine learning for advanced sentiment analysis
