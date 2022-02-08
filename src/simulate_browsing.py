import itertools as it
import os
import random
import signal
import sys
import threading
import time
import typing as t
from contextlib import contextmanager, suppress
from csv import DictReader, DictWriter
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.firefox.service import Service
from urllib3.exceptions import HTTPError, MaxRetryError


@contextmanager
def use_browser(timeout: float):
    # noinspection PyArgumentList
    driver = webdriver.Firefox(service=Service(log_path=os.devnull))
    driver.set_page_load_timeout(timeout)

    try:
        yield driver

    finally:
        with suppress(ConnectionError, MaxRetryError):
            driver.close()


def iter_shuffled_sequence_items_until_keyboard_interrupt(values: t.Collection[str]) -> t.Iterable[str]:
    result = list(values)

    for _ in it.count(1):
        random.shuffle(result)

        yield from result


def simulate(stop, links, delay, timeout, writer):
    with use_browser(timeout) as browser:
        writer.writeheader()

        for link in links:
            if stop.is_set():
                break

            error = None

            now = datetime.utcnow()
            start = time.perf_counter()
            try:
                browser.get(link)

            except TimeoutException as err:
                error = "timeout"

            except WebDriverException as err:
                error = err.msg

            except HTTPError as err:
                error = str(err)

            finally:
                duration = time.perf_counter() - start

            writer.writerow({
                "ts": now.isoformat(timespec="seconds"),
                "link": link,
                "duration": duration,
                "error": error,
            })

            time.sleep(max(delay - duration, 0))


def main(argv: t.Sequence[str]) -> int:
    if "--help" in argv:
        print(f"{argv[0]} PATH DELAY TIMEOUT")
        return 0

    path = Path(argv[1])
    assert path.is_file() and path.exists(), str(path)
    delay = float(argv[2])
    timeout = float(argv[3])

    with path.open("r") as fd:
        links = [
            row["link"]
            for row in DictReader(fd)
        ]

    writer = DictWriter(sys.stdout, ("ts", "link", "duration", "error",))

    stop = threading.Event()
    worker = threading.Thread(
        target=simulate,
        args=(stop, iter_shuffled_sequence_items_until_keyboard_interrupt(links), delay, timeout, writer),
        daemon=True,
    )

    def signal_handler(sig, frame):
        stop.set()
        worker.join(10.0)

    signal.signal(signal.SIGINT, signal_handler)

    worker.start()
    signal.pause()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
