import csv
import os
import typing as t
from contextlib import closing
from pathlib import Path

import pytest
from pytest import fixture
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

F = t.TypeVar("F", bound=t.Callable[..., t.Any])

DATA_DIR = Path(__file__).parent / "data"


@fixture(scope="session")
def browser():
    # noinspection PyArgumentList
    driver = webdriver.Firefox(service=Service(log_path=os.devnull))

    with closing(driver):
        yield driver


def parametrize_from_csv(path: Path, keys: t.Sequence[str]) -> t.Callable[[F], F]:
    with path.open("r") as fd:
        values = [
            tuple(record.get(key) for key in keys)
            for record in csv.DictReader(fd)
        ]

    return pytest.mark.parametrize(argnames=keys, argvalues=values, )
