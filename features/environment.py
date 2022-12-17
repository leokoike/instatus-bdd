from behave import use_fixture
from features.fixtures import get_session


def before_scenario(context, scenario):
    use_fixture(get_session, context)
