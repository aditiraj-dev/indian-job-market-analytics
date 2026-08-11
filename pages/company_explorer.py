import streamlit as st
import pandas as pd
import psycopg2

conn = psycopg2.connect(st.secrets["DB_URL"])

cursor = conn.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())

#-------------------------------------------------------

st.title("Company Explorer")
st.write("Select a company to learn how many jobs were posted (out of 97k posting), and the technologies that are require most.")

all_companies_df = pd.read_sql("""
	SELECT "Companies".company_name, COUNT(*) AS total_jobs
FROM "Companies" JOIN "Jobs" ON "Companies".company_id = "Jobs".company_id
group by "Companies".company_name
having count(*) >= 20
order by total_jobs desc
""", conn)

selected_comp = st.selectbox(
	"Choose a company :",
	all_companies_df["company_name"]
)


total_jobs = pd.read_sql("""
	SELECT COUNT(*) AS no_of_jobs
	FROM "Companies" JOIN "Jobs"
	ON "Companies".company_id = "Jobs".company_id
	WHERE "Companies".company_name = %s
""", conn,
params=[selected_comp])

st.metric(
    "Jobs Posted",
    int(total_jobs.iloc[0]["no_of_jobs"])
)

avg_salary = pd.read_sql("""
SELECT AVG((min_salary + max_salary) / 2.0) AS avg_salary
FROM "Jobs"
JOIN "Companies"
ON "Jobs".company_id = "Companies".company_id
WHERE "Companies".company_name = %s
AND min_salary IS NOT NULL
AND max_salary IS NOT NULL
""",
conn,
params=[selected_comp])

salary = avg_salary.iloc[0]["avg_salary"]

st.metric(
    "Average Salary",
    f"₹{salary:,.0f}" if pd.notna(salary) else "Not Available"
)


related_skills = pd.read_sql("""
	select "Skills".skill_name, COUNT(*) as freq
	from "Companies" join "Jobs" on "Companies".company_id = 	"Jobs".company_id
	join "JobSkills" on "Jobs".job_id = "JobSkills".job_id
	join "Skills" on "JobSkills".skill_id = "Skills".skill_id
	where "Companies".company_name = %s
	group by "Skills".skill_name
	order by freq desc
	limit 50
""", conn,
params=[selected_comp])

st.header(f"Top 50 Skills at {selected_comp}")
st.bar_chart(
	related_skills.set_index("skill_name")
)

st.header("Locations")

