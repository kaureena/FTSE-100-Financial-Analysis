# Logging Rules (How to keep these logs credible)

1) **Write logs as if a reviewer will audit them**
   - Every completed task should reference an *evidence path* in the repo.

2) **Prefer concrete facts**
   - Use dates, run_ids, file paths, and measurable outcomes.

3) **Use London time consistently**
   - Timestamps are Europe/London, not UTC, unless explicitly stated.

4) **Avoid making financial claims**
   - Always include “Not financial advice” where forecasts are mentioned.

5) **Be explicit about limitations**
   - If data is a snapshot, say so.
   - If an event calendar is a stub, say so.
   - If weights are a portfolio demo, say so.

6) **Separate symptoms from root causes**
   - Example: “Parquet write failed” is a symptom; root cause might be “mixed dtypes in timestamp column”.

7) **Close the loop**
   - For every issue closed, include:
     - what was changed
     - how it was verified
     - where the evidence lives
