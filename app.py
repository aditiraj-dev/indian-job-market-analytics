import streamlit as st
import pandas as pd
import psycopg2

from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))

cursor = conn.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())

#-------------------------------------------------------

st.title("Indian Job Market Analytics")

st.write("This is a project done on a dataset on real world 97k+ Indian job postings to learn how to work with a large dataset for the purpose of analysis, and how present those findings, using Streamlit.")

df = pd.read_csv("data/jobs_sample.csv")

st.header("Original Dataset : Sample")
st.dataframe(df.head(20))

query = """
SELECT COUNT(*) AS total_jobs
FROM "Jobs"
"""

df = pd.read_sql(query, conn)

st.write(df)

st.write("The original data was cleaned using Pandas, which included handling missing values, converting data types, standardizing skills, and normalizing locations. The denormalized CSV was then split to create 4 tables in a PostgreSQL database (Companies, Jobs, Skills, JobSkills).")

companies = pd.read_sql(
    'SELECT * FROM "Companies" LIMIT 5',
    conn
)

st.markdown("##### Companies:")
st.dataframe(companies)

jobs = pd.read_sql(
    'SELECT * FROM "Jobs" LIMIT 5',
    conn
)

st.write("##### Jobs:")
st.dataframe(jobs)

skills = pd.read_sql(
    'SELECT * FROM "Jobs" LIMIT 5',
    conn
)

st.write("##### Skills:")
st.dataframe(skills)
#-------------------------------------------------------

st.header("Top 20 Skills")

skills = pd.read_sql("""
SELECT "Skills".skill_name,
       COUNT(*) AS frequency
FROM "JobSkills"
JOIN "Skills"
ON "Skills".skill_id = "JobSkills".skill_id
GROUP BY "Skills".skill_name
ORDER BY frequency DESC
LIMIT 20
""", conn)

st.bar_chart(
    skills.set_index("skill_name")
)

#-------------------------------------------------------

st.header("Top Hiring Companies")

comp = pd.read_sql("""
SELECT "Companies".company_name,
       COUNT(*) AS no_of_jobs
FROM "Companies"
JOIN "Jobs"
ON "Companies".company_id = "Jobs".company_id
GROUP BY "Companies".company_name
ORDER BY no_of_jobs DESC
LIMIT 20
""", conn)

st.bar_chart(comp.set_index("company_name"))

#-------------------------------------------------------

st.header("Jobs by Location")

