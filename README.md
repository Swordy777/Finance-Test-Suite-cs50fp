# Finance P-set Test Suite (CS50 Final Project assignment)
> Since my background is in the quality assurance field, I decided that the best way to exercise everything I learned was by making a project that would be related to testing. My Final Project for [CS50 Course](https://cs50.harvard.edu/x/2023/) is a set of autotests for the last P-set of the course, [Finance](https://cs50.harvard.edu/x/2023/psets/9/finance/).


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
- This project is intended to be a tool that allows one to check if their Finance application adheres to the requirements of the assignment, by expanding and partly overlapping with the set of tests provided by `check50` command
- The purpose of the project is to exercise the abilities of one's Finance application by executing a number of tests that verify the app's behavior in different situations. By analyzing test results, the author can detect and fix bugs in their algorithms and make decisions to improve their project in some aspects. 
- As a quality assurance specialist, I strive to improve in my field of work. Undertaking this project was a great way to get familiar with test automation and programming concepts related to testing. 

This Test Suite consists of over **600+** tests made for different features of the Finance web app. 
This project utilizes Selenium library to emulate user actions in a browser window; allowing to produce and execute various scenarios and test cases. Additionally, Pytest framework allows one to choose specific pre-conditions, levels of logging detail and to decide which sets of tests will be executed. 


## Technologies Used
- Python language
- Pytest framework
- Selenium package for Python
- Additional packages as stated in `requirements.txt`


## Features
- Run tests for different features of the Finance web app together or separately
- Choose which browser would you like to run your tests with
- Choose to enable/disable headless mode for the browser
- Provide access to your SQLite database to run additional database-related tests


## Screenshots
![Example screenshot](./img/screenshot.png)


## Setup
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

- For example, the solution that I used to generate test classes just so fixtures would be called for each set of the parametrized tests doesn't look as succinct and easy to use as desired.
- Related to auto-generated classes from the previous bullet point, it is not yet possible to mark parametrized data sets with pytest.mark for classes that are being created this way.
- Also related to it, sometimes test re-runs with `pytest --lf` do not pick all of the failed tests if they were part of the auto-generated classes.
- Some tests have similar structure and could just be one test with a number of conditionals (potential downsides: test structure might get too complex).
- Referencing test case inputs by using list indexes doesn't look like the most convenient way of handling it.
- and many more...

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
