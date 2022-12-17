from behave import fixture
import requests


@fixture
def get_session(context):
    try:
        context.session = requests.Session()
        yield context.session
    finally:
        context.session.close()
