import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import pytest
from app import app
from extensions import limiter
@pytest.fixture



def client():

    app.config["TESTING"] = True

    old_value = limiter.enabled
    limiter.enabled = False

    with app.test_client() as client:
        yield client

    limiter.enabled = old_value

#enable limiter ony for the testing phase and enable later for the use 