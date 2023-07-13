import pytest
import sqlite3
import re
from uuid import uuid4
from collections import namedtuple
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.firefox.options import Options as ff_options
from werkzeug.security import generate_password_hash

from db_queries import DataBaseQueries
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from constants import DatabaseConstants as DBC, URLS


def check_browser(value):
    """Checks the value of the 'browser' CLI argument"""

    msg = "Received incorrect --browser flag value. Try 'chrome' or 'firefox'"
    if value not in ("chrome", "firefox"):
        raise pytest.UsageError(msg)
    
    return value


def check_db_usage(value):
    """Checks if the user specified the usage of database"""

    msg = "Received incorrect --db-usage flag value. Try 'yes' or 'no'"
    if not (re.fullmatch(r"^[Yy]es", value) or re.fullmatch(r"^[Nn]o", value)):
        raise pytest.UsageError(msg)
    
    return value


def pytest_addoption(parser):
    """
    Adds custom CLI arguments for pytest
    """

    # 'browser' flag. Allows to choose what browser will be used for test execution
    # Available options: 'chrome' and 'firefox'
    parser.addoption("--browser", action="store", default="chrome", 
                     help="Choose a browser to run tests with: '--browser=chrome' or '--browser=firefox'", type=check_browser)
    
    # 'db_usage' flag. If tests have direct access to app's database, can be set to 'yes'. Is off by default
    # Available options: 'yes' and 'no'
    parser.addoption("--db-usage", action="store", default="no", 
                     help="Utilizes app's sqlite database (if accessible) and runs database reliant tests: 'yes' or 'no'", 
                     type=check_db_usage)

    # 'headless' flag. If you don't want tests to display the browser window (and effectively, use gpu), set to 'on'
    # Available options: 'on' and 'off'
    parser.addoption("--headless", action="store_true", 
                     help="use --headless to run driver in headless mode")
    

def pytest_collection_modifyitems(config, items):
    """Adds skip marking db reliant tests if there's no db access to pytest hook"""

    for item in items:
        if not config.getoption("--db-usage").lower() == "yes" and "db_reliant" in item.keywords:
                item.add_marker(pytest.mark.skip(reason="Database is unavailable → skipping this test"))


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
        if request.config.getoption("--headless"):
            options.add_argument("--headless")
        #options.add_argument("--no-sandbox") # Uncomment this line if you want to run tests as root, but it is unsafe!
        browser = webdriver.Chrome(options=options)
    elif browser_type == "firefox":
        options = ff_options()
        if request.config.getoption("--headless"):
            options.add_argument("--headless")
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


@pytest.fixture(autouse=True, scope="session")
def db_available(request):
    """Returns True or False depending on the value of '--db-usage' CLI parameter"""

    if request.config.getoption("--db-usage").lower() == "yes":
         return True
    return False


@pytest.fixture(scope="class")
def database(db_available):
    """
    Fixture that connects do database and initiates a database cursor object.
    Cursor is being passed to the DataBaseQueries class, which contains methods for executing different queries.
    Finally the object of the class is yilded for later use.

    If the user specified that there's no database access, returns None
    """

    if db_available:
        try:
            db = sqlite3.connect(f"file:{DBC.DATABASE_PATH}?mode=rw", # passing path as uri in rw mode so it won't be created
                                uri=True,
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
            
        except sqlite3.Error:
            pytest.fail(
                f"Database at {DBC.DATABASE_PATH} is unavailable; please make sure you have proper access " \
                "or rerun tests with --db-usage=no"
                )
    else:
        yield None


@pytest.fixture(scope="class")
def login_creds():
    """Generates login credentials"""

    Creds = namedtuple('Creds', ['username', 'password'])
    credentials = Creds(f"test-user-{uuid4()}", "P4$$word")

    return credentials


@pytest.fixture(scope="class")
def new_user(browser, database, login_creds, db_available):
    """
    Fixture that registers new user.
    If database can be accessed - simulates registration process and logs in with new creds.
    If not - goes through manual user registration process (calls register_new_user() from RegisterPage class)
    """
    
    if db_available:
        # Insert user data directly into the database
        database.add_new_user(login_creds.username, 
                                      generate_password_hash(login_creds.password, method='pbkdf2:sha256', salt_length=8)
                                      )
        lp = LoginPage(browser, URLS.LOGIN_URL)
        lp.open()
        lp.log_in_with(login_creds.username, login_creds.password)
        assert lp.url_should_change_to(URLS.DEFAULT_URL), (
             "Can't log in, make sure you have proper database access " \
             "or rerun tests with --db-usage=no"
             )

        yield login_creds

        # Delete data from database
        # This clean up segment should delete every row of data associated with the created user in every table 
        # Requires additional queries if database schema is different
        database.delete_tran_data(login_creds.username)
        database.delete_user_data(login_creds.username)
    
    else:
    
        rp = RegisterPage(browser, URLS.REGISTER_URL)
        rp.open()
        rp.register_new_user(login_creds.username, login_creds.password)
     
        assert rp.url_should_change_to(URLS.DEFAULT_URL), (
             "Something went wrong during registration process: " \
             f"current url: {rp.get_current_url()}; expected url: {URLS.DEFAULT_URL}"
             )
        
        yield login_creds


