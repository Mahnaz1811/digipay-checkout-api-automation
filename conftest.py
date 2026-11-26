
import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import APIRequestContext, Playwright


load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "http://localhost:8080")


@pytest.fixture(scope="session")
def cell_number():
    return os.getenv("CELL_NUMBER", "09123456789")


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright, base_url: str):
    request_context = playwright.request.new_context(
        base_url=base_url,
        extra_http_headers={
            "Accept": "application/json",
        },
    )

    yield request_context

    request_context.dispose()
