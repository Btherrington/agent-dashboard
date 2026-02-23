import tweepy
import os
from dotenv import load_dotenv
from database import SessionLocal, Commit

load_dotenv()


client = tweepy.Client(
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
    consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET")
    )

def get_recent_commits(limit):
    db = SessionLocal()
    commits = db.query(Commit).order_by(Commit.date.desc()).limit(limit).all()
    db.close()

    return commits

def generate_post(commit):
    message = f"{commit.repo}, {commit.message}"
    if len(message) > 280:
        message = message[:277] + "..."
    return message

def post_tweet(text):
    try:
        response = client.create_tweet(text=text)
        print(f"Tweet posted: {text}")
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None
    
if __name__ == "__main__":
    recent_commit = get_recent_commits(4)
    if recent_commit:
        generated_post = generate_post(recent_commit[1])
        print(f"Heres the generated tweet: {generated_post}")
        post_tweet(generated_post)

    
        
