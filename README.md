# Finance P-set Test Suite (CS50 Final Project assignment)
> Since my background is in the quality assurance field, I decided that the best way to apply everything I learned was by making a project that would be related to testing. My Final Project for [CS50 Course](https://cs50.harvard.edu/x/2023/) is a set of tests for the last P-set of the course, [Finance](https://cs50.harvard.edu/x/2023/psets/9/finance/).


## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Expected Data Setup](#expected-data-setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)


## General Information
- This project is intended to be a tool that allows one to check if their Finance web application adheres to the requirements of the assignment, by expanding and partly overlapping with the set of tests provided by `check50` command
- The purpose of the project is to exercise the abilities of one's Finance web application by executing a number of tests that verify the app's behavior in different situations. By analyzing test results, the author can detect and fix bugs in their algorithms and make decisions to improve their project in some aspects. 

This Test Suite consists of over **600+** tests made for features of the Finance web app. 
This project utilizes Selenium library to emulate user actions in a browser window; allowing to produce and execute various scenarios and test cases. Additionally, Pytest framework allows one to choose specific pre-conditions, levels of logging detail and to decide which sets of tests will be executed. 


## Technologies Used
- Pytest framework
- Selenium library


## Features
- Run tests for different features of the Finance web app
- Choose which browser you would like to run your tests with
- Choose to enable/disable headless mode for the browser
- Provide access to your SQLite database to run additional database-related tests


## Setup

This project can be used as both a standalone and an addition to an existing Finance project. This depends on if you want to run database-reliant tests or not.
Since you can only access the SQLite database if you have direct access to *.db file, in order for those tests to work you need to have your Test Suite and Finance application in the same folder. If you're only interested in running tests that do not utilize the SQLite database, you can go with the standalone option and just clone the repo locally or create a virtual codespace with the repository checked out.


### Step 1: Setting up the IDE

#### Option 1: Using virtual codespace (independently)

- To create Github virtual codespace with the project checked out, go to the project's page and click Code button, then in the Codespaces tab click "Create codespace on master":
  > <img src="https://github.com/Swordy777/CS50-Final-Project/assets/59532784/50138f0c-58bf-446e-bb87-6bf167deff52" width="350">
- Install Microsoft Python extension (`@id:ms-python.python` in the search bar in the extensions tab)

#### Option 2: Using VS Code desktop (independently)
- Watch and follow the instructions from [this seminar with Carter Zenke](https://cs50.harvard.edu/x/2023/seminars/#developing-your-project-locally-with-vs-code) on how to install VS Code, WSL and set up your project locally or follow the steps below:

  - Download and install [VS Code Desktop](https://code.visualstudio.com/)
  - Install [Windows Subsystem for Linux](https://www.microsoft.com/store/productId/9P9TQF7MRM4R)
  - Install [Ubuntu WSL](https://www.microsoft.com/store/productId/9PDXGNCFSCZV)
  - Go to the Control Panel→Programs→"Turn Windows features on or off", where you'll have to enable the Virtual Machine Platform and Windows Subsystem for Linux options and restart your PC
  - Download and install [Python](https://www.python.org/downloads/)
  - Run the newly installed Ubuntu app (a terminal will show up). Allow it to finish installation and pick a username and password of your choice. Close the terminal
    > If you get the `Failed to attach disk 'LocalState\ext4.vhdx' to WSL2: The system cannot find the file specified.` error, open Powershell and execute:
    > ```
    > wsl --unregister ubuntu
    > wsl --install
    > ```
  - Open VS Code Desktop, and let it connect to WSL
  - Install Microsoft WSL Extension (`ms-vscode-remote.remote-wsl`  in the search bar in the extensions tab) and Microsoft Python extension (`@id:ms-python.python` in the search bar in the extensions tab)
      > If a message that you're on wsl 1 is shown, use [this documentation](https://learn.microsoft.com/en-us/windows/wsl/basic-commands#set-wsl-version-to-1-or-2) to switch to wsl 2
  - Press Ctrl + Shift + P → WSL: Open folder in WSL, then pick "Show Local" and choose a folder for the project. Press <code>Ctrl + `</code> to display a terminal and check if it runs on Powershell; if it does, press Ctrl + Shift + P again and pick WSL: Reopen folder in WSL. This time after VS Code restarts your terminal should use bash
- Enable Ubuntu repositories:
  >```
  >sudo add-apt-repository main
  >sudo add-apt-repository universe
  >sudo add-apt-repository restricted
  >sudo add-apt-repository multiverse
  >```
- Go to the project page, and click the Code button, then in the Local tab click Github CLI and copy the CLI command for repo cloning:
  > <img src="https://github.com/Swordy777/CS50-Final-Project/assets/59532784/7d469a2f-7957-4493-b483-1cac4d432000" width="350">
- Paste the command into your bash terminal and execute it.
  > If necessary, install `gh` package and go through Github's authentication process

#### Option 3: Adding tests to an existing project (if you already have your IDE setup)
- Download Test Suite as *.zip file and unzip it the way you prefer (by using the VS Code GUI or `unzip` command) to your current project repo, be it in a virtual codespace or in VS Code desktop
  > <img src="https://github.com/Swordy777/CS50-Final-Project/assets/59532784/35674f55-9ff6-40fb-b3e8-d0afe40f818f" width="350">


### Step 2: Creating and enabling a virtual environment

Just so you wouldn't have to manage all of your installed packages all at once, and to avoid any conflicts, create a virtual environment:
- Make sure you're in a bash terminal 
- Execute the following command: `python -m venv name-your-venv`
  > if you get
  > ```
  > Command 'python' not found, did you mean:
  > command 'python3' from deb python3
  > command 'python' from deb python-is-python3
  > ```
  > error, execute the following command: `alias python='python3'`.
  > If prompted to install venv package, execute the suggested command, for example `sudo apt install python3.10-venv`
- Activate your environment: `source name-your-venv/bin/activate`. Your command line will have a (name-your-venv) prefix if everything succeeds.


### Step 3: Installing packages
- Make sure you're in the folder with the project files
- Install required packages with `pip install -r requirements.txt`
  > Install pip with `sudo apt install python3-pip` if prompted

### Step 4: Installing Chrome and Firefox
- Make sure you're in the folder with the project files
- Execute Chrome installation script `bash install-chrome.sh`
- To install Firefox, execute `sudo apt-get install firefox` command
> If Firefox installed the way above isn't working correctly, execute `sudo apt purge firefox` and try to run the installation script `bash install-firefox.sh`
> Alternatively, to uninstall Firefox that was installed by install-firefox.sh, execute:
> ```
> sudo rm -r /etc/alternatives/firefox
> sudo rm /usr/bin/firefox
> ```


### Optional: Setup X11 forwarding to watch tests execute in browser window (for virtual codespace only)

>Virtual codespace doesn't allow to run GUI applications. This means if you choose to work with this project by using virtual codespace, you will have two options:
> 1. You can only run tests using `--headless` CLI argument (look for the details in the **Usage** section)
> 2. If you want to see tests execute in browser, follow the instructions below.
- Execute `sudo apt-get install xbase-clients` in your virtual codespace
- Download and install [Github CLI](https://cli.github.com/)
- Download and install [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
- Run Xserver (Xlaunch); during the setup process just click 'Next' until it's finished; give access if prompted
- Run cmd.exe
- In the command line:
  - Execute:
    ```
    setx DISPLAY "127.0.0.1:0.0"
    gh cs ssh -- -XY
    ```
  - If prompted, authorize; pick your codespace in the list of available codespaces.
  - Check your DISPLAY environment variable: `echo $DISPLAY`. If it isn’t set, execute `export DISPLAY=localhost:10.0`
  - Activate venv from Step 2
  - Run tests :)


## Expected Data Setup

By default, this Test Suite is set up for testing the Finance web application created by the CS50 team, https://finance.cs50.net

In reality, everyone's implementation will more or less vary. To address some of the inconsistencies, this project has a number of files that prepare some static data:

### Constants
`constants.py` file contains parameter sets for test cases and most of the static data, like the URL for the application, available routes, table header names, etc. Please edit it accordingly so each of the variables defined here matches your implementation.
  > But how do I figure out what's the URL for my Finance web application after I deploy it with `flask run`?
  > After your web app is deployed, you will usually get a URL in the terminal:
  > ![image](https://github.com/Swordy777/Finance-Test-Suite-cs50fp/assets/59532784/7100cf48-287c-4990-86f2-7d6811ca1b03)
  > Notice, that the domain name ends with a certain number - it is the port that is used to host the app.
  > Don't forget to set port visibility to public, so the tests can access it:
  > 
  > <img src="https://github.com/Swordy777/Finance-Test-Suite-cs50fp/assets/59532784/8e12a338-88ca-4aa5-b65b-ba801d2c1c8a" width="350">

### Locators
`/pages/locators.py` contains unique locators for most of the elements present on the application's pages. Please check that current locators match your webpage elements, so tests can correctly detect interact with them (also, this is a great practice in learning how CSS and XPath selectors work!).

### Database queries
`db_queries.py` contains all of the database queries that are used to run database-related tests. These particular queries apply to a db schema designed for my implementation of Finance. Sorry, spoilers! But designing a database isn't the only thing you'll have to do to finish this P-set. You can either use these queries to kind of get an idea of what the initial schema looked like and adjust it for queries, or you can exercise your SQL skills and rewrite all of the queries so they would fit your own database schema.


## Usage

By simply going to the folder with tests and running `pytest` in terminal window, pytest will collect all of the tests in the current directory and execute them.
  > If for any reason this doesn't work for you, try to invoke it like this: `python -m pytest ...`

Tests can also be run for each of the modules. For example `pytest test_buy_page.py` will only run tests stored in `test_buy_page.py` module

To run tests from a specific class, specify it after the module name separated with two colons: 
```
pytest test_default_page.py::TestDefaultTableBehaviour
```

You can also run a specific test from a class, just add another double-colon separator: 
```
pytest test_navigation.py::TestNavigationStructureAuthed::test_cs50logo_is_visible
```

Pytest has some useful CLI arguments, like:
- `-s` - allows for print() statements to display data in the terminal (useful for debugging)
- `-v` - verbose, allows one to see detailed messages in various aspects
- `-tb` - traceback, allows one to choose how detailed is the error message in case of a failed test, for example `--tb=line` only shows one line per failure

Besides existing CLI arguments for Pytest, I added a couple of custom ones:
### --headless
> Runs browser in headless mode, by default it's off. This means that instead of displaying the browser window, tests will execute in the background, for example: `pytest test_sell_page.py --headless`

> [!IMPORTANT]
> When using this project in a virtual codespace, ALWAYS use this tag, unless you've set up the X11 solution from above.
### --browser
> Allows to choose the browser to run tests. By default it's Chrome, so executing `pytest -s -v --tb=line test_quote_page.py --browser=firefox` will run Quote Page tests in Firefox

### --db-usage
> Can be set to 'yes' and 'no'; is off by default. Run with 'yes' if you're positive you have access to the app's database, and the path to it is specified in `constants.py`. For example, to run tests for successful registration, you can execute:
> ```
> pytest -s -v test_register_page.py::TestSuccesfullRegistration --db-usage=yes

You can combine custom CLI arguments, for example:
```
pytest -s -v --tb=long test_history_page.py::TestHistoryTableDataDependencies --headless --db-usage=yes
```
will run all of the tests in the class `TestHistoryTableDataDependencies()` from `test_history_page.py` module with access to database, in headless mode in Chrome

To learn how to invoke pytest in more details, go [here](https://docs.pytest.org/en/7.1.x/how-to/usage.html#usage)


## Project Status
_complete_

This project might be far from perfect, but this version felt like a reasonable point to finish development.


## Room for Improvement
Of course, as with any project, it has room for improvement. Here's a couple of ideas to improve the project:

- For example, the solution that I used to generate test classes just so fixtures would be called for each set of the parametrized tests isn't as simple and easy to use as desired.
- Related to auto-generated classes from the previous bullet point, it is not yet possible to mark parametrized data sets with pytest.mark (in other words to mark some of the parameters from a range as expected to fail, etc.) for such classes.
- Also related to first bullet point, sometimes test re-runs with `pytest --lf` do not pick all of the failed tests if some of them were auto-generated.
- Some tests have similar structure and could just be one test with a number of conditionals (potential downsides: test structure might get too complex).
- Referencing test case parameter sets by using list indexes doesn't look like the most convenient way of handling it.
- Firefox installation script might do more harm than good and is subject to analysis.

## Acknowledgements
- The base of this project is the knowledge provided by the [CS50 Course](https://cs50.harvard.edu/x/2023/)
- Pytest and Selenium knowledge and techniques based on [this Stepik course](https://stepik.org/course/575/promo#toc) (ru-lang only)
- An important solution to the problem of not being able to call fixtures for each of the parametrized sets of tests from [this topic on pytest's github discussions page](https://github.com/pytest-dev/pytest/discussions/11038)
- A ton of different stackoverflow topics like: [not being able to type emojis with Selenium in Chrome](https://stackoverflow.com/questions/59138825/chromedriver-only-supports-characters-in-the-bmp-error-while-sending-emoji-with), [zipping dictionaries by key matches](https://stackoverflow.com/questions/29645415/python-zip-by-key), etc.
- Instruction on how to [install Google Chrome on WSL](https://cloudbytes.dev/snippets/run-selenium-and-chrome-on-wsl2), [install Firefox on WSL](https://linuxconfig.org/how-to-install-uninstall-and-update-firefox-on-ubuntu-20-04-focal-fossa-linux), [run GUI apps in virtual codespace](https://babyprogrammer.com/blog/running-gui-code-applications-in-github-codespaces-on-windows/), etc.
- Different documentation available on the net, like [the sqlite3 library for python](https://docs.python.org/3/library/sqlite3.html), [pytest documentation](https://docs.pytest.org/en/7.1.x/index.html), [experimenting and learning more of the regular expressions](https://docs.python.org/3/library/re.html), [getting more familiar with dictionary methods](https://www.w3schools.com/python/python_dictionaries_methods.asp), [learning more about css and xpath selectors](https://www.w3schools.com/cssref/css_selectors.php), and many more



## Contact
Created by [@Andrei Zorin](mailto:swordy777@gmail.com) - feel free to contact me!
