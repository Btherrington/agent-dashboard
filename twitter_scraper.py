import tweepy
import os
from dotenv import load_dotenv
import requests
from database import SessionLocal, Tweet
import time

load_dotenv()

client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN")
)

handle_dict = {
    "alphatrends": None,
    "TheStalwart": None,
    "StockMktTV": None,
    "Venu_7_": None,
    "TheDonInvesting": None,
    "nullcharts": None,
    "jmoneystonks": None,
    "ChartsJavi": None,
    "StocktonKatie": None,
    "standuquesne": None,
    "d_gilz": None,
    "JSpitTrades": None,
    "Citrini7": None,
    "ConnorJBates_": None,
    "ezcontra": None,
    "sstrazza": None,
    "fejau_inc": None,
    "lBattleRhino": None,
    "JC_ParetsX": None,
    "Bluntz_Capital": None,
    "jam_croissant": None,
    "Tradermayne": None,
    "naval": None,
    "Marsgains1": None,
    "CarpeNoctom": None,
    "JamesClear": None,
    "NavalismHQ": None

}


def fetch_latest_tweets():
    db = SessionLocal()
    for name in handle_dict:
        try:
            user_tweets = client.get_users_tweets(id=handle_dict[name], max_results=5, tweet_fields=["created_at"])
            for returned_tweet_data in user_tweets.data:
                tweet_check = Tweet(
                    id=str(returned_tweet_data.id),
                    handle=name,
                    text=returned_tweet_data.text,
                    date=returned_tweet_data.created_at
                )
                db.merge(tweet_check)
            db.commit()
            print(f"Got tweets from @{name}")
        except Exception as e:
            print(f"Error fetching @{name}: {e}")
        time.sleep(950)
    db.close()


def cache_users_ids():
    for name in handle_dict:
        if handle_dict[name] is None:
            try:
                user = client.get_user(username=name)
                handle_dict[name] = str(user.data.id)
                print(f"'{name}': '{user.data.id}',")
            except Exception as e:
                print(f"Error: {name}: {e}")
            time.sleep(900)
    


if __name__ == "__main__":
    from database import init_db
    init_db()
    cache_users_ids() 
    fetch_latest_tweets()
    

        



