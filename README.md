# PRPay

PR Pay is a tool that encourages your team members to participate in reviews by providing "bounty-like" rewards to early reviewers and participants. Access is simple, login with your Github account and monitor your inbox for when you're requested for a review. Once you review a PR it becomes claimable. Add your Coinbase wallet address for ethereum testnet and you'll recieve your bounty!

## Setup
To configure a Github repository you need to add two webhooks:
1. PR Modification Webhook
  * Payload URL: https://prpay.api.kanishkkacholia.com/webhooks/github/pull-request
  * Content Type: application/json
  * Select Individual Events (only choose Pull Requests)

2. PR Creation Webhook
  * Payload URL: https://prpay.api.kanishkkacholia.com/webhooks/github/pull-request-review
  * Content Type: application/json
  * Select Individual Events (only choose Pull Request Reviews)
