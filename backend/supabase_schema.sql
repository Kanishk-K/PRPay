-- PRPay Database Schema
-- Run this in Supabase SQL Editor to create the database structure

-- Create enum type for review status
CREATE TYPE review_status AS ENUM (
    'requested',
    'claimable',
    'claimed',
    'ineligible',
    'done'
);

-- Users table (stores GitHub user information)
CREATE TABLE users (
    github_user_id TEXT PRIMARY KEY,
    username TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Pull Requests table
CREATE TABLE pull_requests (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    body TEXT,
    url TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- User PR Reviews (M2M relationship table)
CREATE TABLE user_pr_reviews (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(github_user_id) ON DELETE CASCADE,
    pr_id INTEGER NOT NULL REFERENCES pull_requests(id) ON DELETE CASCADE,
    status review_status NOT NULL DEFAULT 'requested',
    payout DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, pr_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_user_pr_reviews_user_id ON user_pr_reviews(user_id);
CREATE INDEX idx_user_pr_reviews_pr_id ON user_pr_reviews(pr_id);
CREATE INDEX idx_user_pr_reviews_status ON user_pr_reviews(status);
CREATE INDEX idx_user_pr_reviews_user_status ON user_pr_reviews(user_id, status);

-- Add comments for documentation
COMMENT ON TABLE users IS 'GitHub users who review pull requests';
COMMENT ON TABLE pull_requests IS 'Pull requests that can be reviewed';
COMMENT ON TABLE user_pr_reviews IS 'Many-to-many relationship tracking user reviews of PRs with payout information';
COMMENT ON COLUMN user_pr_reviews.status IS 'Current status: requested, claimable, claimed, ineligible, or done';
COMMENT ON COLUMN user_pr_reviews.payout IS 'Payout amount in dollars for this review';
