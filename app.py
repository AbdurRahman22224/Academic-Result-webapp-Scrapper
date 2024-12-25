import streamlit as st
import pandas as pd
from scrape import download_driver, generate_roll_number, scrape_results
import time
import json

# Streamlit UI
st.set_page_config(
   page_title = "Result Scraper",
   page_icon = ":chart_with_upwards_trend:",
   initial_sidebar_state = "expanded",
)
st.title("Scrape Result Data")
# Dropdown for Branch, Sem, and Year
branch = st.selectbox("Select Branch", ["CS", "EC", "EE", "ME" ,"PI", "MM", "CE", "CM"])
sem = st.selectbox("Select Semester", ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'])
year = st.selectbox("Select Year", [2021, 2022, 2023, 2024])
course = st.selectbox("Select Course", ['UG'])
num_of_stu = st.text_input("Number of Students", value="61")
num_stu = int(num_of_stu)
# Start scraping button
if st.button("Start Scraping"):
    # Initialize the driver
    driver = download_driver()
    results = []
    result_placeholder = st.empty()

    # Loop through and scrape for all the students
    for i in range(30, num_stu):

        roll_no = generate_roll_number(branch, year, course, i)
        name, sgpa, cgpa = scrape_results(driver, roll_no, sem)

        # Append results
        if name and sgpa and cgpa:
            results.append({"Roll No": roll_no, "Name": name, "SGPA": sgpa, "CGPA": cgpa})
        else:
            results.append({"Roll No": roll_no, "Name": "Not Found", "SGPA": "Not Found", "CGPA": "Not Found"})
        
   
        # Update the table in the placeholder
        result_placeholder.write(pd.DataFrame(results))

    # Save results to a JSON file
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)

    st.success("Scraping Complete!")

