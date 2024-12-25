---

# Scraping Project

This project is a web scraping application designed to scrape results from my institute's result published website. It utilizes `Selenium` for browser automation.
- [Clone the Repository](#clone-the-repository)
- [Install Dependencies](#install-dependencies)
- [Run the Application](#run-the-application)

---

## Clone the Repository

To clone this repository, use the following command:

```bash
git clone https://github.com/AbdurRahman22224/Academic-Result-webapp-Scrapper.git
```

Navigate to the project directory:

```bash
cd Academic-Result-webapp-Scrapper
```

---

## Install Dependencies

Before running the project, you need to install the required dependencies. You can install them using `pip`.

1. **Create a Virtual Environment** (optional but recommended):

    ```bash
    python -m venv venv
    ```

2. **Activate the Virtual Environment**:
   
    - **Windows**:
        ```bash
        venv\Scripts\activate
        ```

3. **Install the Required Packages**:

    Use the following command to install all dependencies:

    ```bash
    pip install -r requirements.txt
    ```

---

## Run the Application

Once the dependencies are installed, you can run the scraping application using:

```bash
streamlit run app.py
```

This will start the scraper and begin scraping data as defined in the script.

---

### Additional Configuration

- **Chrome WebDriver**: Ensure that you have a valid Chrome WebDriver installed on your system. You can install it using `ChromeDriverManager` if not already installed.

---
