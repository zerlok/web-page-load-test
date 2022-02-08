from contextlib import closing

from pytest import fixture
from selenium import webdriver


@fixture(scope="session")
def browser():
    with closing(webdriver.Firefox()) as result:
        yield result
