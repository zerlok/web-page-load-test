import os
from contextlib import closing

from pytest import fixture
from selenium import webdriver


@fixture(scope="session")
def browser():
    with closing(webdriver.Firefox(service_log_path=os.devnull)) as result:
        yield result
