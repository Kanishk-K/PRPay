from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from routers import webhooks_router, reviews_router

app = FastAPI(title="PRPay API", version="1.0.0")

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhooks_router)
app.include_router(reviews_router)


@app.get("/")
def root():
    return {
        "message": "PRPay API",
        "version": "1.0.0",
        "endpoints": {
            "GET /getPRs": "Get PR reviews for a user",
            "POST /claimPR": "Claim a PR review",
            "POST /webhooks/github/pull-request": "GitHub webhook endpoint",
        },
    }
