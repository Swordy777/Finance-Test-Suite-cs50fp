import pytest
import sqlite3
from uuid import uuid4
from collections import namedtuple
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.firefox.options import Options as ff_options
from werkzeug.security import check_password_hash, generate_password_hash

from db_queries import DataBaseQueries
from pages.register_page import RegisterPage
from pages.urls import URLS


# Path to app's database file. By default is set to the mock database
DATABASE_PATH = "mock.db"


def check_browser(value):
    """Checks the value of the 'browser' CLI argument"""

    msg = "Received incorrect --browser flag value. Try 'chrome' or 'firefox'"
    if value not in ("chrome", "firefox"):
        raise pytest.UsageError(msg)
    
    return value


def pytest_addoption(parser):
    """
    Adds a custom 'browser' CLI argument for pytest
    Available options: 'chrome' and 'firefox'
    """

    parser.addoption("--browser", action="store", default="chrome", 
                     help="Choose a browser to run tests with: '--browser=chrome' or '--browser=firefox'", type=check_browser)


@pytest.fixture(autouse=True, scope="class")
def browser(request):
    """
    Autouse fixture.
    Initiates a browser driver object
    """
    
    browser_type = request.config.getoption("--browser")
    if browser_type == "chrome":
        options = chrome_options()
        options.add_argument("--disable-gpu")
        #options.add_argument("--no-sandbox") # Uncomment this line if you want to run tests as root, but it is unsafe!
        browser = webdriver.Chrome(options=options)
    elif browser_type == "firefox":
        options = ff_options()
        #options.add_argument("-kiosk") # Fullscreen mode for Firefox. Uncomment if you want it enabled
        browser = webdriver.Firefox(options=options) # Remeber that you can't run Firefox as root
    browser.maximize_window()

    yield browser

    browser.quit()


@pytest.fixture(autouse=True)
def skip_by_browser(request):
    """Helper fixture for skipping firefox or chrome specific tests"""

    if request.config.getoption("--browser") == "chrome":
        if request.node.get_closest_marker('firefox_only'):
                pytest.skip('This test is for Firefox browser.')  
    elif request.config.getoption("--browser") == "firefox":
        if request.node.get_closest_marker('chrome_only'):
                pytest.skip('This test is for Chrome browser.')  


@pytest.fixture(scope="class")
def database():
    """
    Fixture that initiates a database cursor object.
    Then it is being passed to the DataBaseQueries class.
    The class contains methods for executing different queries.
    Finally the object of the class is yilded for later use.
    """

    db = sqlite3.connect(DATABASE_PATH, 
                         isolation_level=None,  # Turns autocommit mode on for sqlite3, 
                                                # i.e all changes are commited immediately
                         check_same_thread=True # Makes sure connection is only used by the thread that created it
                         )
    
    # Query results are returned as Row objects, which allow to access values using keys as in dictionaries
    # For more info: https://docs.python.org/3/library/sqlite3.html#sqlite3.Row 
    db.row_factory = sqlite3.Row 

    database = DataBaseQueries(db.cursor())

    yield database

    db.close()


@pytest.fixture(scope="class")
def login_creds():
    """Generates login credentials"""

    Creds = namedtuple('Creds', ['username', 'password'])
    credentials = Creds(f"test-user-{uuid4()}", "P4$$word")

    return credentials


@pytest.fixture(scope="class")
def new_user(browser, database, login_creds):
    """
    Fixture that registers new user.
    Mostly repeats the steps of 'successfull registration' test.
    """
    
    rp = RegisterPage(browser, URLS.REGISTER_URL)
    rp.open()
    rp.register_new_user(login_creds.username, login_creds.password)

    # Insert data into mock database (should comment this line if using app's db, since it adds the user itself) 
    database.mock_db_add_new_user(login_creds.username, 
                                  generate_password_hash(login_creds.password, method='pbkdf2:sha256', salt_length=8)
                                  )
    
    assert rp.url_should_change_to(URLS.DEFAULT_URL), "Something went wrong during the registration process"

    yield login_creds

    # Delete data from database
    # This clean up segment should delete every row of data associated with the created user in every table 
    # Requires additional queries if database schema is different
    database.mock_db_delete_tran_data(login_creds.username)
    database.mock_db_delete_user_data(login_creds.username)
