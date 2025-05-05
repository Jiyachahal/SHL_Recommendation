# 🛍️ Product Recommender System

An AI-powered product recommender system built with Django, featuring a custom-trained machine learning model that suggests relevant products based on user input. The system includes a web scraping component to gather product data and is deployed at: [https://jiyachahal23.pythonanywhere.com/](https://jiyachahal23.pythonanywhere.com/).

---

## 📦 Project Overview

- **Web Scraping**: Utilizes `scraper.py` to extract product data from target websites.
- **Data Storage**: Stores scraped data in `shl_catalog_full.csv`.
- **Machine Learning**: Employs BOW and cosine similarity to recommend products.
- **Web Interface**: Provides a user-friendly interface built with Django.
- **Deployment**: Hosted on PythonAnywhere for public accessibility.

---

## 🗂️ Project Structure
- **Database Folder**: Holds the python program used to scrape , the data base created .
- **Myproject Folder**: Holds the Django Web project ( and webapp recommmendations)
- **SHL_Model_jupyter Folder**: Holds notebook used to do  data processing, apply model  and evaluate perfomace .
