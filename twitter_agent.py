import tweepy
import os
from dotenv import load_dotenv
from database import SessionLocal, Commit
import requests

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
    try:
        ollama_response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.1:8b",
            "prompt": f"{commit.repo}, {commit.message}, Rewrite this as a casual tweet about the topic and any nuance that can be found. Assume your audience isnt aware of what your posting about, respond as a solo developer, no hashtags or enthusiasm/performative behavior, but give it some substance and expand on it if possible, give it a bit of a story, use correct capitalization. Keep it under 280 characters",
            "stream": False
        })
        tweet = ollama_response.json()["response"]
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        return tweet
    except:
        return f"{commit.repo}, {commit.message}"


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
        generated_post = generate_post(recent_commit[0])
        print(f"Heres the generated tweet: {generated_post}")
        #post_tweet(generated_post)

    
        
