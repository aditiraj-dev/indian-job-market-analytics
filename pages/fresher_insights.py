import streamlit as st	
import pandas as pd
import psycopg2

conn = psycopg2.connect(st.secrets["DB_URL"])

cursor = conn.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())

#-------------------------------------------------------

st.title("Fresher Insights")

avg_salary_df = pd.read_sql("""
SELECT AVG((min_salary + max_salary) / 2.0) AS avg_salary
FROM "Jobs"
WHERE max_experience = 0
AND min_salary IS NOT NULL
AND max_salary IS NOT NULL;
""", conn)

avg_salary = avg_salary_df.iloc[0]["avg_salary"]


st.metric(
    "Average Fresher Salary",
    f"₹{avg_salary:,.0f}" if pd.notna(avg_salary) else "Not Available"
)

top_skills = pd.read_sql("""
select "Skills".skill_name, COUNT(*) as freq
from "Jobs" join "JobSkills" on "Jobs".job_id = "JobSkills".job_id
join "Skills" on "JobSkills".skill_id = "Skills".skill_id
where "Jobs".max_experience <= 1
group by "Skills".skill_name
order by freq desc
LIMIT 50
""", conn)

st.header("Top Skills")
st.bar_chart(
	top_skills.set_index("skill_name")
)

top_companies = pd.read_sql("""
select "Companies".company_name, COUNT(*) as freq
from "Companies" join "Jobs" on "Companies".company_id = "Jobs".company_id
where "Jobs".max_experience <= 1
group by "Companies".company_name
order by freq desc
LIMIT 50
""", conn)

st.header("Top Companies")
st.bar_chart(
	top_companies.set_index("company_name")
)