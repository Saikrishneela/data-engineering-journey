# Data Engineering Journey

My hands-on journey from full-stack developer to data engineer. Each folder is one learning stage, built as working code, not just notes.

I learn by building small pipelines, then combining them into real projects.

## What I've Built So Far

| Folder | What it covers |
|---|---|
| `day-02` | Customer ETL in Python: reads CSV, cleans fields (trim, lowercase emails, age check), validates (missing values, duplicate IDs, invalid emails) and writes clean and invalid files |
| `day-03` | Python + PostgreSQL: connecting with Psycopg, parameterized queries, UPSERTs, transactions and commits |
| `day-04` | Orders dataset used for the validation and loading pipeline |
| `[folder name]` | Orders ETL pipeline: validates orders, rejects bad rows with a reason, UPSERTs clean rows into PostgreSQL and verifies the load |

## Skills Practised

- **Python for data work:** CSV handling, cleaning, validation, reject handling, reusable functions
- **SQL and PostgreSQL:** joins, GROUP BY, CTEs, window functions, UPSERTs, transactions, indexes, `EXPLAIN` / `EXPLAIN ANALYZE`
- **ETL:** extract, validate, transform, load, verify
- **Data modeling:** OLTP vs OLAP, star schema, fact and dimension tables, grain, surrogate keys, SCD Type 1 and 2
- **Git and GitHub:** a branch per learning stage, meaningful commits, pull requests

## Roadmap

- [x] Python for data engineering
- [x] SQL and PostgreSQL
- [x] Python + PostgreSQL ETL
- [x] Data modeling and warehouse design
- [ ] PySpark (in progress)
- [ ] Apache Airflow
- [ ] Cloud (AWS)
- [ ] Kafka and streaming
- [ ] Data quality and CI/CD
- [ ] Projects 2 and 3

## How to Run the Code

1. Clone the repo:

```bash
git clone https://github.com/Saikrishneela/data-engineering-journey.git
cd data-engineering-journey
```

2. Install the dependency:

```bash
pip install "psycopg[binary]"
```

3. Set your database password as an environment variable (never hardcode it):

```bash
# Windows PowerShell
$env:POSTGRES_PASSWORD="your_password"

# Mac / Linux
export POSTGRES_PASSWORD="your_password"
```

4. Open a day's folder and run its script, for example:

```bash
cd day-02
python customer_etl.py
```

Some scripts expect a local PostgreSQL database named `de_learning`.

## Tech Stack

Python, SQL, PostgreSQL, Psycopg, PySpark (learning), Git, GitHub

## About Me

Saikrishna Kanukuntla, Python developer moving into data engineering.

- LinkedIn: https://www.linkedin.com/in/saikrishna-kanukuntla-8b518422a
- GitHub: https://github.com/Saikrishneela
- LeetCode: https://leetcode.com/u/SaikrishnaS/
- Email: saikrishnaprince24@gmail.com

I'm documenting this journey on LinkedIn as I go. Feedback is welcome.
