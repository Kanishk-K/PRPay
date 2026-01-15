-- ========================================
-- PRPay Complete Database Setup Script
-- ========================================
-- Run this entire script in Supabase SQL Editor
-- It will create tables, add mock data, and disable RLS for development

-- STEP 1: Create enum type for review status
-- ========================================
CREATE TYPE review_status AS ENUM (
    'requested',
    'claimable',
    'claimed',
    'ineligible',
    'done'
);

-- STEP 2: Create tables
-- ========================================

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

-- STEP 3: Create indexes for better query performance
-- ========================================
CREATE INDEX idx_user_pr_reviews_user_id ON user_pr_reviews(user_id);
CREATE INDEX idx_user_pr_reviews_pr_id ON user_pr_reviews(pr_id);
CREATE INDEX idx_user_pr_reviews_status ON user_pr_reviews(status);
CREATE INDEX idx_user_pr_reviews_user_status ON user_pr_reviews(user_id, status);

-- STEP 4: Disable Row Level Security for development
-- ========================================
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE pull_requests DISABLE ROW LEVEL SECURITY;
ALTER TABLE user_pr_reviews DISABLE ROW LEVEL SECURITY;

-- STEP 5: Insert mock data
-- ========================================

-- Insert mock users
INSERT INTO users (github_user_id, username, created_at) VALUES
('user1', 'alice_dev', NOW() - INTERVAL '30 days'),
('user2', 'bob_reviewer', NOW() - INTERVAL '25 days'),
('user3', 'charlie_coder', NOW() - INTERVAL '20 days'),
('user4', 'diana_engineer', NOW() - INTERVAL '15 days'),
('user5', 'evan_developer', NOW() - INTERVAL '10 days');

-- Insert mock pull requests
INSERT INTO pull_requests (title, body, url, created_at) VALUES
('Add user authentication system', 'Implements OAuth 2.0 flow with JWT tokens', 'https://github.com/example/repo/pull/101', NOW() - INTERVAL '28 days'),
('Fix memory leak in data processor', 'Resolves issue #234 by properly disposing resources', 'https://github.com/example/repo/pull/102', NOW() - INTERVAL '26 days'),
('Update React components to TypeScript', 'Migrates all components from JS to TS for better type safety', 'https://github.com/example/repo/pull/103', NOW() - INTERVAL '24 days'),
('Implement dark mode toggle', 'Adds theme switching functionality with persistent storage', 'https://github.com/example/repo/pull/104', NOW() - INTERVAL '22 days'),
('Optimize database queries', 'Reduces query time by 60% through indexing and query optimization', 'https://github.com/example/repo/pull/105', NOW() - INTERVAL '20 days'),
('Add unit tests for API endpoints', 'Achieves 90% test coverage for REST API', 'https://github.com/example/repo/pull/106', NOW() - INTERVAL '18 days'),
('Refactor authentication middleware', 'Simplifies auth logic and improves error handling', 'https://github.com/example/repo/pull/107', NOW() - INTERVAL '16 days'),
('Implement file upload feature', 'Adds drag-and-drop file upload with progress tracking', 'https://github.com/example/repo/pull/108', NOW() - INTERVAL '14 days'),
('Fix CSS styling issues on mobile', 'Resolves responsive design problems on small screens', 'https://github.com/example/repo/pull/109', NOW() - INTERVAL '12 days'),
('Add email notification system', 'Sends automated emails for important events', 'https://github.com/example/repo/pull/110', NOW() - INTERVAL '10 days'),
('Upgrade dependencies to latest versions', 'Updates all npm packages and fixes breaking changes', 'https://github.com/example/repo/pull/111', NOW() - INTERVAL '8 days'),
('Implement search functionality', 'Adds full-text search with filters and pagination', 'https://github.com/example/repo/pull/112', NOW() - INTERVAL '6 days'),
('Add user profile page', 'Creates customizable user profile with avatar upload', 'https://github.com/example/repo/pull/113', NOW() - INTERVAL '4 days'),
('Fix security vulnerability in login', 'Patches XSS vulnerability in login form', 'https://github.com/example/repo/pull/114', NOW() - INTERVAL '2 days'),
('Improve error handling in API', 'Adds consistent error responses across all endpoints', 'https://github.com/example/repo/pull/115', NOW() - INTERVAL '1 day');

-- Insert mock user PR reviews with various statuses (all payouts = $1.00)

-- user1 reviews (mix of all statuses)
INSERT INTO user_pr_reviews (user_id, pr_id, status, payout, timestamp) VALUES
('user1', 1, 'done', 1.00, NOW() - INTERVAL '27 days'),
('user1', 2, 'done', 1.00, NOW() - INTERVAL '25 days'),
('user1', 3, 'claimed', 1.00, NOW() - INTERVAL '23 days'),
('user1', 4, 'claimable', 1.00, NOW() - INTERVAL '21 days'),
('user1', 5, 'claimable', 1.00, NOW() - INTERVAL '19 days'),
('user1', 6, 'requested', 1.00, NOW() - INTERVAL '17 days');

-- user2 reviews
INSERT INTO user_pr_reviews (user_id, pr_id, status, payout, timestamp) VALUES
('user2', 2, 'done', 1.00, NOW() - INTERVAL '24 days'),
('user2', 4, 'done', 1.00, NOW() - INTERVAL '20 days'),
('user2', 6, 'claimed', 1.00, NOW() - INTERVAL '16 days'),
('user2', 7, 'claimable', 1.00, NOW() - INTERVAL '15 days'),
('user2', 8, 'claimable', 1.00, NOW() - INTERVAL '13 days'),
('user2', 9, 'requested', 1.00, NOW() - INTERVAL '11 days'),
('user2', 10, 'ineligible', 1.00, NOW() - INTERVAL '9 days');

-- user3 reviews
INSERT INTO user_pr_reviews (user_id, pr_id, status, payout, timestamp) VALUES
('user3', 1, 'done', 1.00, NOW() - INTERVAL '26 days'),
('user3', 5, 'claimed', 1.00, NOW() - INTERVAL '18 days'),
('user3', 9, 'claimable', 1.00, NOW() - INTERVAL '10 days'),
('user3', 11, 'claimable', 1.00, NOW() - INTERVAL '7 days'),
('user3', 12, 'requested', 1.00, NOW() - INTERVAL '5 days'),
('user3', 13, 'requested', 1.00, NOW() - INTERVAL '3 days');

-- user4 reviews
INSERT INTO user_pr_reviews (user_id, pr_id, status, payout, timestamp) VALUES
('user4', 3, 'done', 1.00, NOW() - INTERVAL '22 days'),
('user4', 7, 'claimed', 1.00, NOW() - INTERVAL '14 days'),
('user4', 10, 'claimable', 1.00, NOW() - INTERVAL '8 days'),
('user4', 13, 'claimable', 1.00, NOW() - INTERVAL '2 days'),
('user4', 14, 'requested', 1.00, NOW() - INTERVAL '1 day'),
('user4', 15, 'ineligible', 1.00, NOW() - INTERVAL '12 hours');

-- user5 reviews
INSERT INTO user_pr_reviews (user_id, pr_id, status, payout, timestamp) VALUES
('user5', 8, 'claimed', 1.00, NOW() - INTERVAL '12 days'),
('user5', 11, 'claimable', 1.00, NOW() - INTERVAL '6 days'),
('user5', 14, 'claimable', 1.00, NOW() - INTERVAL '1 day'),
('user5', 15, 'requested', 1.00, NOW() - INTERVAL '6 hours');

-- ========================================
-- SETUP COMPLETE!
-- ========================================
-- Summary:
-- ✓ Created enum type: review_status
-- ✓ Created 3 tables: users, pull_requests, user_pr_reviews
-- ✓ Created indexes for performance
-- ✓ Disabled RLS for development
-- ✓ Inserted 5 users
-- ✓ Inserted 15 pull requests
-- ✓ Inserted 30 review records
--
-- Status distribution:
--   - requested: 8
--   - claimable: 10
--   - claimed: 6
--   - ineligible: 2
--   - done: 4
-- ========================================
