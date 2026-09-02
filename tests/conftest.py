"""
conftest.py

Shared pytest fixtures.
"""

import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def checkn_cache_path(tmp_path_factory: pytest.TempPathFactory):
    """
    Redirect checkn's persistent cache to a throwaway file for the whole
    test session, so running the suite never touches or mutates the
    developer's real ~/.checkn_cache.db.
    """
    cache_path = tmp_path_factory.mktemp("checkn_cache") / "test_cache.db"
    old = os.environ.get("CHECKN_CACHE_PATH")
    os.environ["CHECKN_CACHE_PATH"] = str(cache_path)
    yield cache_path
    if old is None:
        os.environ.pop("CHECKN_CACHE_PATH", None)
    else:
        os.environ["CHECKN_CACHE_PATH"] = old
