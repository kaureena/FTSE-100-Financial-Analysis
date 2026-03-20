# Security

This project is an **offline-first portfolio** repo.

## Data sources

- V1 runs can use the **repo snapshot provider** to avoid external calls.
- V2 defaults to synthetic generation.

If you enable any live providers (Yahoo/Polygon/AlphaVantage), treat API keys as secrets:

- store in environment variables
- never commit `.env` files
