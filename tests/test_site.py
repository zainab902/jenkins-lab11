import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8090")


@pytest.fixture
def driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--user-data-dir=/tmp/chrome-profile")
    drv = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    yield drv
    drv.quit()


def test_page_title(driver):
    driver.get(BASE_URL)
    assert driver.title == "CSC418 Lab 11"


def test_main_heading(driver):
    driver.get(BASE_URL)
    heading = driver.find_element(By.ID, "main-heading")
    assert heading.text == "Deployed by a CI/CD Pipeline"


def test_student_name_is_set(driver):
    driver.get(BASE_URL)
    text = driver.find_element(By.ID, "student").text
    assert text.startswith("Student: ")
    assert "YOUR NAME" not in text


def test_button_shows_message(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "greet").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "message"), "Hello")
    )
    assert driver.find_element(By.ID, "message").text == "Hello from the pipeline!"
    driver.save_screenshot("screenshot.png")
