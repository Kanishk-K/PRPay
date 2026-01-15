# PRPay Backend Setup Guide

This guide will help you set up the PRPay backend API with Supabase PostgreSQL database.

## Prerequisites

- Python 3.10 or higher
- A Supabase account (free tier works fine)
- pip or pipenv for package management

## Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 2: Set Up Supabase Database

### 2.1 Create a Supabase Project

1. Go to [https://app.supabase.com](https://app.supabase.com)
2. Click "New Project"
3. Fill in project details and wait for it to be created

### 2.2 Run Database Schema

1. In your Supabase dashboard, go to the **SQL Editor**
2. Create a new query
3. Copy the contents of `supabase_schema.sql` and paste it into the editor
4. Click "Run" to create the tables and enum types

### 2.3 Add Mock Data

1. Still in the **SQL Editor**, create another new query
2. Copy the contents of `seed_data.sql` and paste it into the editor
3. Click "Run" to populate the database with mock data

This will create:
- 5 mock users (user1-user5)
- 15 mock pull requests
- 30 review records with various statuses

## Step 3: Configure Environment Variables

1. Copy the `.env` file template
2. Fill in your Supabase credentials:

```bash
# Get these from your Supabase project settings
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key-here
DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:[PORT]/postgres
```

### How to Find Your Credentials:

1. **SUPABASE_URL**:
   - Go to Settings > API > Project URL

2. **SUPABASE_SERVICE_KEY**:
   - Go to Settings > API > service_role key (Click "Reveal" button)
   - ⚠️ Keep this secret! Don't commit it to git

3. **DATABASE_URL** (optional, for direct SQL connections):
   - Go to Settings > Database > Connection String > URI
   - Copy the URI format and replace `[YOUR-PASSWORD]` with your database password

## Step 4: Run the API Server

```bash
# From the backend directory
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Step 5: Test the API

### View API Documentation

Open your browser to:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Test Endpoints

#### Get PRs for a user:
```bash
# Get all PRs for user1
curl "http://localhost:8000/getPRs?user_id=user1"

# Get only claimable PRs for user1
curl "http://localhost:8000/getPRs?user_id=user1&status=claimable"
```

#### Claim a PR:
```bash
curl -X POST "http://localhost:8000/claimPR" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user1", "pr_id": 4}'
```

## API Endpoints

### `GET /getPRs`

Get PR reviews for a specific user.

**Query Parameters:**
- `user_id` (required): GitHub user ID
- `status` (optional): Filter by status (requested, claimable, claimed, ineligible, done)

**Example Response:**
```json
[
  {
    "pr_id": 4,
    "pr_title": "Implement dark mode toggle",
    "pr_body": "Adds theme switching functionality with persistent storage",
    "pr_url": "https://github.com/example/repo/pull/104",
    "pr_created_at": "2025-12-24T10:30:00Z",
    "review_id": 4,
    "user_id": "user1",
    "status": "claimable",
    "payout": 1.0,
    "review_timestamp": "2025-12-25T10:30:00Z"
  }
]
```

### `POST /claimPR`

Claim a PR review (status must be "claimable").

**Request Body:**
```json
{
  "user_id": "user1",
  "pr_id": 4
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "PR successfully claimed",
  "review_id": 4,
  "status": "claimed"
}
```

**Error Response (not claimable):**
```json
{
  "success": false,
  "message": "Cannot claim PR. Current status is 'claimed', must be 'claimable'",
  "review_id": 4,
  "status": "claimed"
}
```

## Mock Data Overview

### Users:
- `user1` (alice_dev) - 6 reviews
- `user2` (bob_reviewer) - 7 reviews
- `user3` (charlie_coder) - 6 reviews
- `user4` (diana_engineer) - 6 reviews
- `user5` (evan_developer) - 4 reviews

### Review Status Distribution:
- **requested**: 8 reviews
- **claimable**: 10 reviews (ready to be claimed!)
- **claimed**: 6 reviews
- **ineligible**: 2 reviews
- **done**: 4 reviews

## Database Schema

### Tables:

1. **users**
   - `github_user_id` (TEXT, PRIMARY KEY)
   - `username` (TEXT)
   - `created_at` (TIMESTAMPTZ)

2. **pull_requests**
   - `id` (SERIAL, PRIMARY KEY)
   - `title` (TEXT)
   - `body` (TEXT)
   - `url` (TEXT)
   - `created_at` (TIMESTAMPTZ)

3. **user_pr_reviews**
   - `id` (SERIAL, PRIMARY KEY)
   - `user_id` (TEXT, FOREIGN KEY → users)
   - `pr_id` (INTEGER, FOREIGN KEY → pull_requests)
   - `status` (review_status ENUM)
   - `payout` (DECIMAL)
   - `timestamp` (TIMESTAMPTZ)

## Project Structure

```
backend/
├── main.py              # FastAPI application with endpoints
├── database.py          # Supabase client initialization
├── models.py            # Pydantic models for data validation
├── schemas.py           # Request/response schemas
├── enums.py             # ReviewStatus enum definition
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (DO NOT COMMIT)
├── supabase_schema.sql  # Database schema creation script
├── seed_data.sql        # Mock data insertion script
└── SETUP.md            # This file
```

## Troubleshooting

### Error: "Supabase credentials not found"
- Make sure your `.env` file exists in the `backend/` directory
- Check that `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` are set correctly

### Error: "relation does not exist"
- Make sure you ran `supabase_schema.sql` in the Supabase SQL Editor
- Check that you're connected to the correct Supabase project

### No data returned from `/getPRs`
- Make sure you ran `seed_data.sql` to populate the database
- Verify the data exists by checking the Supabase Table Editor

### CORS errors from frontend
- The backend is configured to allow `localhost:3000` and `localhost:3001`
- If your frontend runs on a different port, update the CORS settings in `main.py`

## Next Steps for Frontend Integration

Your frontend engineer can now:

1. Call `GET /getPRs?user_id=user1` to fetch PR reviews
2. Call `POST /claimPR` to claim reviews
3. Filter by status using the `status` query parameter
4. Use the Swagger UI at `/docs` to explore the API interactively

All payouts are currently hardcoded to $1.00 as requested.
