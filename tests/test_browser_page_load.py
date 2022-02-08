import pytest
from pytest import fixture

from conftest import DATA_DIR, parametrize_from_csv


@fixture()
def page_loader(browser):
    def load(link) -> bool:
        browser.get(link)
        return True

    return load


@pytest.mark.benchmark(
    group="browser-page-load",
    warmup=True,
)
@parametrize_from_csv(DATA_DIR / "links.csv", "link")
def test_page_link_load(benchmark, page_loader, link):
    benchmark(page_loader, link)
