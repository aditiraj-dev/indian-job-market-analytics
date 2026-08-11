import streamlit as st	
import pandas as pd
import psycopg2

conn = psycopg2.connect(st.secrets["DB_URL"])

cursor = conn.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())

#-------------------------------------------------------

st.title("Skill Explorer")


st.write("Select a skill to learn which companies require it, and the technologies that are commonly appear alongside it.")

all_skills_df = pd.read_sql("""
	SELECT skill_name FROM "Skills"
	ORDER BY skill_name
""", conn)

selected_skill = st.selectbox(
	"Choose a skill :",
	all_skills_df["skill_name"]
)

st.write("P E N D I N G")