# Selenium tests run by the Jenkins pipeline (headless Chromium inside Docker)
import os, pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = os.environ.get("APP_URL", "http://localhost:8081")

@pytest.fixture()
def d():
    o = Options()
    for a in ("--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1100,650"):
        o.add_argument(a)
    o.binary_location = "/usr/bin/chromium"
    drv = webdriver.Chrome(options=o)
    yield drv
    drv.quit()

def login(d, u, p):
    d.get(BASE + "/index.html")
    d.find_element(By.ID, "username").send_keys(u)
    d.find_element(By.ID, "password").send_keys(p)
    d.find_element(By.ID, "loginBtn").click()

def test_login_page_title(d):
    d.get(BASE + "/index.html")
    assert d.title == "Gem Store - Login"

def test_invalid_login(d):
    login(d, "student", "wrong")
    assert d.find_element(By.ID, "message").text == "Invalid username or password"

def test_valid_login(d):
    login(d, "student", "test123")
    WebDriverWait(d, 10).until(EC.url_contains("shop.html"))
    assert "Welcome, student" in d.find_element(By.ID, "welcome").text

def test_contact_validation(d):
    d.get(BASE + "/contact.html")
    d.find_element(By.ID, "submitBtn").click()
    assert d.find_element(By.ID, "result").text == "All fields are required"

def test_contact_submit(d):
    d.get(BASE + "/contact.html")
    d.find_element(By.ID, "name").send_keys("Manan")
    d.find_element(By.ID, "email").send_keys("manan@example.com")
    d.find_element(By.ID, "msg").send_keys("Hello")
    d.find_element(By.ID, "submitBtn").click()
    assert d.find_element(By.ID, "result").text == "Thank you Manan, your message has been submitted."
