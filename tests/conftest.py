import csv
import os
import typing as t
from contextlib import closing
from pathlib import Path

import pytest
from pytest import fixture
from selenium import webdriver

F = t.TypeVar("F", bound=t.Callable[..., t.Any])

DATA_DIR = Path(__file__).parent / "data"


@fixture(scope="session")
def browser():
    with closing(webdriver.Firefox(service_log_path=os.devnull)) as result:
        yield result


def parametrize_from_csv(path: Path, key: str) -> t.Callable[[F], F]:
    with path.open("r") as fd:
        values = [
            record[key]
            for record in csv.DictReader(fd)
            if key in record
        ]

    return pytest.mark.parametrize(argnames=(key,), argvalues=[(value,) for value in values], )
