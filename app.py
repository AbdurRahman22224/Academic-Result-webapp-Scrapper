import streamlit as st
import pandas as pd
from scrape import download_driver, generate_roll_number, scrape_results, genrate_subjects
from selenium.common.exceptions import NoSuchElementException
import json
from selenium.webdriver.common.by import By


# Streamlit UI
st.set_page_config(
   page_title = "Result Scraper",
   page_icon = ":chart_with_upwards_trend:",
   initial_sidebar_state = "expanded",
)
st.title("Scrape Result Data")
# Dropdown for Branch, Sem, and Year
branch = st.selectbox("Select Branch", ["PI","CS", "EC", "EE", "ME", "MM", "CE", "CM"])
sem = st.selectbox("Select Semester", ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII','VIII'])
year = st.selectbox("Select Year", [2021, 2022, 2023, 2024])
course = st.selectbox("Select Course", ['UG'])
num_of_stu = st.text_input("Strength", value="61")
num_stu = int(num_of_stu)

driver = download_driver()

def scrape_marks(driver, sub_name):
    marks = []
    i = 2  # Starting index (adjust based on your observation)
    for i in range(2, len(sub_name) + 2):
        try:
            xpath = f'//*[@id="PnlShowResult"]/table/tbody/tr[4]/td/table/tbody/tr[{i}]/td[8]'
            element = driver.find_element("xpath", xpath)
            marks.append(element.text)
            i += 1
        except NoSuchElementException:
            break  # Exit loop when there are no more subject rows
    return marks

subjects = None
# Start scraping button
if st.button("Start Scraping"):

    # Initialize the driver
    results = []
    result_placeholder = st.empty()

    # Loop through and scrape for all the students
    for i in range(1, num_stu):

        roll_no = generate_roll_number(branch, year, course, i)
        name, sgpa, cgpa = scrape_results(driver, roll_no, sem)
         # Get subject names only once
        if subjects is None:
            subjects = genrate_subjects(driver)
            # print("Fetched subjects list:", subjects)  Debug print
        marks = scrape_marks(driver, subjects)

        # Append results
        
        if name and sgpa and cgpa:
            subject_marks = dict(zip(subjects, marks))
            # subject_mark_dict = {f"Sub_{sub}": mark for sub, mark in zip(subjects, marks)}
            results.append({
                "Roll No": roll_no,
                "Name": name,
                "SGPA": sgpa,
                "CGPA": cgpa,
                **subject_marks
            })

        else:
            results.append({"Roll No": roll_no, "Name": "Not Found", "SGPA": "Not Found", "CGPA": "Not Found"})
        
   
        # Update the table in the placeholder
        result_placeholder.write(pd.DataFrame(results))

    # Save results to a JSON file
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)

    st.success("Scraping Complete!")
