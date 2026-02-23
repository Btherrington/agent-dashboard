from fastapi import FastAPI
import httpx
import os
from dotenv import load_dotenv
from database import init_db, SessionLocal, Commit
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from twitter_agent import get_recent_commits, generate_post, post_tweet

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

init_db()

@app.get("/health")
def health_check():
    return {"status": "running"}

@app.get("/repos")
async def get_repos():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
        )
        repos = response.json()
        return [{"name": r["name"], "url": r["html_url"]} for r in repos]

@app.get("/commits")
async def get_commits():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
        )
        repos = response.json()

        all_commits = []
        for repo in repos:
            commits_response = await client.get(
                f"https://api.github.com/repos/{repo['full_name']}/commits",
                headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
                params={"per_page": 5}
            )
            commits = commits_response.json()
            for c in commits:
                commit_obj = Commit(
                    id=c["sha"],
                    repo=repo["name"],
                    message=c["commit"]["message"],
                    date=datetime.fromisoformat(c["commit"]["author"]["date"].replace("Z", "+00:00"))
                )
                db = SessionLocal()
                db.merge(commit_obj)
                db.commit()
                db.close()

                all_commits.append({
                    "repo": repo["name"],
                    "message": c["commit"]["message"],
                    "date": c["commit"]["author"]["date"]
                })

        return all_commits


@app.get("/stored-commits")
def get_stored_commits():
    db = SessionLocal()
    commits = db.query(Commit).all()
    db.close()
    return [
        {
            "repo": c.repo,
            "message": c.message,
            "date": str(c.date)
        }
        for c in commits
    ]


@app.get("/generate-post")
def set_twitter_repo():
    commits = get_recent_commits(1)
    generated_post = generate_post(commits[0])
    return generated_post


@app.post("/post-tweet")
def post_on_twitter(text: str):
    tweet_posted = post_tweet(text)
    if tweet_posted:
        return {"status": "posted", "tweet": tweet_posted}
    return {"status": "failed"}
