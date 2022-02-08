import pytest
from pytest import fixture


@fixture(params=(
        "http://www.python.org",
        "http://google.com",
))
def page_link(request):
    return request.param


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
def test_page_link_load(benchmark, page_loader, page_link):
    benchmark(page_loader, page_link)
