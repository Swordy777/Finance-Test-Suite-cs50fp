import time
import os
import sys
import pytest
import errno
import sqlite3
from uuid import uuid4


from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.firefox.options import Options as ff_options

from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.urls import URLS

DEFAULT_USER = "swordy"
DEFAULT_PASSWORD = "123"

def check_browser(value):
    msg = "Received incorrect --browser flag value. Try 'chrome' or 'firefox'"
    if value not in ("chrome", "firefox"):
        raise pytest.UsageError(msg)
    return value

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", 
                     help="Choose a browser to run tests with: '--browser=chrome' or '--browser=firefox'", type=check_browser)

@pytest.fixture(autouse=True)
def browser(request):
    browser_type = request.config.getoption("--browser")
    if browser_type == "chrome":
        options = chrome_options()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox") # Uncomment this line if you can only run tests as root, but it is unsafe!
        browser = webdriver.Chrome(options=options)
    elif browser_type == "firefox":
        options = ff_options()
        #options.add_argument("-kiosk") # Fullscreen mode for Firefox. Uncomment if you want it enabled
        browser = webdriver.Firefox(options=options) # Remeber that Firefox doesn't allow to run itself as root
    browser.maximize_window()
    yield browser
    browser.quit()

@pytest.fixture
def database():

    db = sqlite3.connect("mock.db", 
                         isolation_level=None, # TODO: add description of the parameter
                         check_same_thread=False # TODO: add description of the parameter
                         )
    db.row_factory = sqlite3.Row # For more info: https://docs.python.org/3/library/sqlite3.html#sqlite3.Row
    cur = db.cursor()
    yield cur
    db.close()

@pytest.fixture
def user():
    user = {"username":f"testuser-{uuid4()}", "password":"P4$$word"}
    return user

@pytest.fixture
def new_user(browser, database, user):
    rp = RegisterPage(browser, URLS.REGISTER_URL)
    rp.open()
    rp.register_new_user(user['username'], user['password'])
    # Insert data into mock database (should comment this line if using a real database, since it already adds the user) 
    rp.query(database, "Insert into users (username, password) values (?, ?);", user['username'], user['password'])
    rp.url_should_change_to(URLS.DEFAULT_URL)
    yield user
    # Delete data from mock database (should be replaced with real one)
    # This clean up segment should delete every row of data associated with the created user in every table 
    # Here I use two tables; your implementation may be different
    rp.query(database, "Delete from purchases where user_id in (Select id from users where username = ?);", user['username'])
    rp.query(database, "Delete from users where username = ?;", user['username'])

@pytest.fixture()
def login(browser, request):
    username = request.node.get_closest_marker("un")
    if username is None:
        username = DEFAULT_USER
    else:
        username = username.args[0]
    password = request.node.get_closest_marker("pw")
    if password is None:
        password = DEFAULT_PASSWORD
    else:
        password = password.args[0]
    login_page = LoginPage(browser, URLS.LOGIN_URL)
    login_page.open()
    login_page.log_in_with(username, password)
    assert login_page.url_should_change_to(URLS.DEFAULT_URL), (
        f"Expected to be redirected to default page after logging in; current page: {login_page.browser.current_url}")