import pytest
import time
from collections import namedtuple

def generate_tests_cls_parametrize(cls: type, parameter_names: str, values: list[tuple]):
    """
    https://github.com/pytest-dev/pytest/discussions/11038
    Implemented class generation solution from topic above (with little changes)
    Usually it is enough to parametrize tests with @pytest.mark.parametrize(),
    but for some tests of mine it is important for fixtures defined in conftest.py
    to be called before each set of the parametrized tests.
    Atm if you have a class-scoped fixture, it is only set up before all sets of tests,
    and torn down after all sets.
    This solutions generates a class for each parametrization option you have,
    allowing conftest.py fixtures to be set up and torn down before and after each parametrized test set.
    """

    parameters = parameter_names.split(", ")
    def generate_fixture(someparam):
        @pytest.fixture(scope="class")
        def my_fixture(self):
            return someparam
        return my_fixture
    base_cls_name = "Test" + cls.__name__.removeprefix("Base").removesuffix("Test")
    gen_classes = {}
    for test_values in values:
        name_suffix = "[" + "-".join(str(value) for value in test_values) + "]"
        cls_name = base_cls_name + name_suffix 
        newclass = type(
            cls_name,
            (cls,),
            {
                parameter_name: generate_fixture(value)
                for parameter_name, value in zip(parameters, test_values, strict=True)
            },
        )
        gen_classes.update({cls_name:newclass})
    return gen_classes


def setup_page(class_name, browser, link):
    """Reusable page setup; allows to pick a scope for each clas depending on test conditions"""

    page = class_name(browser, link)
    page.open()
    return page


def compare_time(t1, tdiff=2, delay=5):
    """
    Compares t1 argument with current time.
    tdiff - difference between current timezone and t1's timezone in hours (default: 2)
    delay - tolerated error for calculated difference in seconds (default: 5)
    """
    
    t1 = time.strptime(t1, "%Y-%m-%d %H:%M:%S")
    t2 = time.localtime()
    if len(t1) == len(t2):
        for i in range(len(t1)):
            if i == 3:
                if t1[i] - (t2[i] - tdiff) != 0:
                    return False
            elif i == 5:
                if abs(t1[i] - t2[i]) > delay:
                    return False
            elif i == 8:
                pass
            else:
                if t1[i] - t2[i] != 0:
                    return False
        return True
    return False


def zip_by_key(actual, expected):
    """Creates a list of tuples only of values from two dictionaries which have the same key"""
    
    combined = namedtuple('combined', ['key', 'actual', 'expected'])

    matches = [combined(k, actual[k], v) for (k, v) in expected.items() if k in actual]
    return matches

