from behave import *
import requests

API_URL = "https://api.instatus.com/v1/clal3my5c74002hqocl2gxbjzr"
AUTH = {"Authorization": "Bearer ae51773af66a984727f5354eef70165f"}
GET_ALL = 1
GET_ONE = 2
SAVE = 3
DELETE = 4

STATUS = 1
JSON = 2


@given("initialize")
def step_initialize(context):
    pass


@when("get_incidents")
def step_when_get_all(context):
    resposta = requests.get(f"{API_URL}/incidents", headers=AUTH)
    context.response = {
        GET_ALL: {
            STATUS: resposta.status_code,
            JSON: resposta.json(),
        }
    }


@when("verify_size_list")
def step_when_verify(context):
    assert context.response is not None


@when("not_empty_list")
def step_when_not_empty_list(context):
    assert context.response is not None


@when("view_incident_details")
def step_when_view_incident(context):
    incident_id = context.response[GET_ALL][JSON][0]["id"]
    resposta = requests.get(f"{API_URL}/incidents/{incident_id}", headers=AUTH)
    context.response[GET_ONE] = {
        STATUS: resposta.status_code,
        JSON: resposta.json(),
    }


@when("delete_a_incident_from_list")
def step_when_delete_from_list(context):
    incident_id = context.response[GET_ALL][JSON][-1]["id"]
    resposta = requests.delete(f"{API_URL}/incidents/{incident_id}", headers=AUTH)
    context.response[DELETE] = {
        STATUS: resposta.status_code,
        JSON: resposta.json(),
    }


@when("exit_system")
def step_exit(context):
    pass


@then("notEmptyList")
def step_then_not_empty_list(context):
    assert len(context.response[GET_ALL][JSON]) != 0


@then("incidentActiveSuccess")
def step_then_incident_sucess(context):
    assert context.response[GET_ONE][STATUS] == 200
    assert (
        context.response[GET_ONE][JSON]["id"]
        == context.response[GET_ALL][JSON][0]["id"]
    )


@then("deleteSuccess")
def step_then_delete_sucess(context):
    assert context.response[DELETE][STATUS] == 200
    assert (
        context.response[DELETE][JSON]["id"]
        == context.response[GET_ALL][JSON][-1]["id"]
    )
