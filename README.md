# Finance P-set Test Suite (CS50 Final Project assignment)
> Since my background is in the quality assurance field, I decided that the best way to apply everything I learned was by making a project that would be related to testing. My Final Project for [CS50 Course](https://cs50.harvard.edu/x/2023/) is a set of autotests for the last P-set of the course, [Finance](https://cs50.harvard.edu/x/2023/psets/9/finance/).


## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
<!-- * [License](#license) -->


## General Information
- This project is intended to be a tool that allows one to check if their Finance web application adheres to the requirements of the assignment, by expanding and partly overlapping with the set of tests provided by `check50` command
- The purpose of the project is to exercise the abilities of one's Finance web application by executing a number of tests that verify the app's behavior in different situations. By analyzing test results, the author can detect and fix bugs in their algorithms and make decisions to improve their project in some aspects. 
- As a quality assurance specialist, I strive to improve in my field of work. Undertaking this project was a great way to get familiar with test automation and programming concepts related to testing. 

This Test Suite consists of over **600+** tests made for features of the Finance web app. 
This project utilizes Selenium library to emulate user actions in a browser window; allowing to produce and execute various scenarios and test cases. Additionally, Pytest framework allows one to choose specific pre-conditions, levels of logging detail and to decide which sets of tests will be executed. 


## Technologies Used
- Pytest framework
- Selenium library package for Python
- Additional packages as stated in `requirements.txt`


## Features
- Run tests for different features of the Finance web app together or separately
- Choose which browser you would like to run your tests with
- Choose to enable/disable headless mode for the browser
- Provide access to your SQLite database to run additional database-related tests


## Screenshots
![Example screenshot](./img/screenshot.png)


## Setup

This project can be used as both a standalone and an addition to an existing Finance project. This depends on if you want to run database-reliant tests or not.
Since you can only access Sqlite database if you have direct access to *.db file, in order for those tests to work you will have to have your Test Suite and Finance application in the same repo, same folder. If you're only interested in running tests that do not utilize Sqlite database, you can just clone the repo locally or create a virtual codespace with repository checked out.

### Setting up the IDE

#### Using virtual codespace (standalone)

- To create Github virtual codespace with the project checked out, go to the project's page and click Code button, then in the Codespaces tab click "Create codespace on master"
![scr1](https://github.com/Swordy777/CS50-Final-Project/assets/59532784/50138f0c-58bf-446e-bb87-6bf167deff52)
- Codespace might recommend you to install Microsoft Python extension (@id:ms-python.python in the search input on extensions tab). Proceed with installing it.

#### Using VS Code desktop (standalone)
- Download and install [VS Code Desktop](https://code.visualstudio.com/)
- Download and install [WSL from Microsoft Store](https://www.microsoft.com/store/productId/9P9TQF7MRM4R)
- Go to the Control Panel, click Programs, and then click Turn Windows features on or off
- Enable the Virtual Machine Platform option. 
- Enable the Windows Subsystem for Linux option.
- Open VS Code Desktop
- 

#### Adding tests to existing project
- Open your Github virtual codespace with your current project repo checked out, download Test Suite as *.zip file and unzip it the way you prefer (by using the VS Code GUI or `unzip` command)
![image](https://github.com/Swordy777/CS50-Final-Project/assets/59532784/35674f55-9ff6-40fb-b3e8-d0afe40f818f)


- To create Github virtual codespace with the project checked out, go to the project's page and click Code button, then in the Codespaces tab click "Create codespace on master"
![Example screenshot](https://i.ibb.co/hZ2xvqt/scr1.png)
- Codespace might recommend you to install Microsoft Python extension (@id:ms-python.python in the search input on extensions tab). Proceed with installing it.


  
#### Creating and enabling virtual environment

Just so you wouldn't have to manage all of your installed packages all at once, and to avoid any conflicts, create a virtual environment:
- Make sure it's a bash terminal 
- Execute the following command: `python -m venv nameofyourvenv`
- And then activate your environment: `source nameofyourvenv/bin/activate`. Your command line will have a (nameofyourvenv) prefix if everything succeeds.

#### Installing packages
- Make sure you're in the folder with the project files
- Install required packages with `pip install -r requirements.txt`

#### Installing Chrome and Firefox
- Make sure you're in the folder with the project files
- Execute Chrome installation script `bash install-chrome.sh`
- Execute Firefox installation script `bash install-firefox.sh`






What are the project requirements/dependencies? Where are they listed? A requirements.txt or a Pipfile.lock file perhaps? Where is it located?

Proceed to describe how to install / setup one's local environment / get started with the project.


## Usage
How does one go about using it?
Provide various use cases and code examples here.

`write-your-code-here`


## Project Status
_complete_

This project might be far from perfect, but this version felt like a reasonable point to finish development.


## Room for Improvement
Of course, as with any project, it has room for improvement. Here's a couple of ideas to improve the project:

- For example, the solution that I used to generate test classes just so fixtures would be called for each set of the parametrized tests isn't as simple and easy to use as desired.
- Related to auto-generated classes from the previous bullet point, it is not yet possible to mark parametrized data sets with pytest.mark (in other words to mark some of the parameters from a range as expected to fail, etc.) for classes that are being created this way.
- Also related to it, sometimes test re-runs with `pytest --lf` do not pick all of the failed tests if some of them were auto-generated.
- Some tests have similar structure and could just be one test with a number of conditionals (potential downsides: test structure might get too complex).
- Referencing test case inputs by using list indexes doesn't look like the most convenient way of handling it.
- Firefox installation process was discovered by trials and errors, and may not be the best way to do it

## Acknowledgements
- The base of this project is the knowledge provided by the [CS50 Course](https://cs50.harvard.edu/x/2023/)
- Pytest and Selenium knowledge and techniques based on [this Stepik course](https://stepik.org/course/575/promo#toc) (ru-lang only)
- An important solution to the problem of not being able to call fixtures for each of the parametrized sets of tests from [this topic on pytest's github discussions page](https://github.com/pytest-dev/pytest/discussions/11038)
- A ton of different stackoverflow topics like: [not being able to type emojis with Selenium in Chrome](https://stackoverflow.com/questions/59138825/chromedriver-only-supports-characters-in-the-bmp-error-while-sending-emoji-with), [zipping dictionaries by key matches](https://stackoverflow.com/questions/29645415/python-zip-by-key), etc.
- Different documentation available on the net, like [the sqlite3 library for python](https://docs.python.org/3/library/sqlite3.html), [pytest documentation](https://docs.pytest.org/en/7.1.x/index.html), [experimenting and learning more of the regular expressions](https://docs.python.org/3/library/re.html), [getting more familiar with dictionary methods](https://www.w3schools.com/python/python_dictionaries_methods.asp), [learning more about css and xpath selectors](https://www.w3schools.com/cssref/css_selectors.php), and many more
- Many thanks to [David J. Mallan](https://cs.harvard.edu/malan/) and the team behind the [CS50 Course](https://cs50.harvard.edu/x/2023/) for making learning fun and giving this spark of creativity a proper headstart!


## Contact
Created by [@Andrei Zorin](mailto:swordy777@gmail.com) - feel free to contact me!

<!-- MIT License -->
