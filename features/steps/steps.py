from behave import *
import string
import random
from datetime import datetime

API_URL = "https://api.instatus.com/v1/clal3my5c74002hqocl2gxbjzr"
AUTH = {"Authorization": "Bearer ae51773af66a984727f5354eef70165f"}

# keywords para salvar a resposta das requisições
GET_ALL = 1  # guarda a lista de incidents
GET_ONE = 2  # guarda um incident recuperado
SAVE = 3  # guarda o incident que foi atualizado/criado
DELETE = 4  # guarda o incident que foi deletado
ERROR = 5  # guarda os dados de erro

STATUS = 1  # status code da request
JSON = 2  # corpo da resposta
VAR = 3  # variavel auxiliar


def generate_post_random_data() -> dict:
    data = {
        "name": generate_random_string(),
        "message": "Este incidente foi adicionado via teste da api",
        "components": ["clal3my5v74030hqocw29ekqla"],
        "started": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "INVESTIGATING",
        "notify": True,
        "statuses": [{"id": "clal3my5v74030hqocw29ekqla", "status": "OPERATIONAL"}],
    }

    return data


def generate_post_random_data_error() -> dict:
    data = {
        "name": generate_random_string(),
        "message": "Este incidente foi adicionado via teste da api",
        "components": ["teste"],
        "started": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "INVESTIGATING",
        "notify": True,
        "statuses": [{"id": "clal3my5v74030hqocw29ekqla", "status": "OPERATIONAL"}],
    }

    return data


def generate_put_random_data() -> dict:
    data = {
        "name": generate_random_string(),
        "components": ["clal3my5v74030hqocw29ekqla"],
        "status": "INVESTIGATING",
        "notify": True,
        "statuses": [{"id": "clal3my5v74030hqocw29ekqla", "status": "OPERATIONAL"}],
    }

    return data


def generate_put_random_data_error() -> dict:
    data = {
        "name": generate_random_string(),
        "components": ["teste"],
        "status": "INVESTIGATING",
        "notify": True,
        "statuses": [{"id": "clal3my5v74030hqocw29ekqla", "status": "OPERATIONAL"}],
    }

    return data


def generate_random_string() -> str:
    letras = string.ascii_lowercase
    random_str = "".join(random.choice(letras) for _ in range(8))

    return random_str


@given("initialize_not_empty_list")
def step_given_init_not_empty(context):
    resposta = context.session.get(f"{API_URL}/incidents", headers=AUTH)
    assert resposta.status_code == 200
    if len(resposta.json()) == 0:
        context.session.post(
            f"{API_URL}/incidents", headers=AUTH, json=generate_post_random_data()
        )

        resposta = context.session.get(f"{API_URL}/incidents", headers=AUTH)
        assert resposta.status_code == 200

    context.response = {
        GET_ALL: {
            STATUS: resposta.status_code,
            JSON: resposta.json(),
            VAR: len(resposta.json()),
        }
    }


@given("initialize_empty_list")
def step_given_init_empty(context):
    resposta = context.session.get(f"{API_URL}/incidents", headers=AUTH)
    assert resposta.status_code == 200
    context.response = {}
    lista_itens = resposta.json()
    if len(lista_itens) != 0:
        for item in lista_itens:
            id = item["id"]
            context.session.delete(f"{API_URL}/incidents/{id}", headers=AUTH)

        resposta = context.session.get(f"{API_URL}/incidents", headers=AUTH)
        assert resposta.status_code == 200

    context.response = {
        GET_ALL: {
            STATUS: resposta.status_code,
            JSON: resposta.json(),
            VAR: len(resposta.json()),
        }
    }


@when("get_incidents")
def step_when_get_all(context):
    resposta = context.session.get(f"{API_URL}/incidents", headers=AUTH)
    assert resposta.status_code == 200
    context.response[GET_ALL] = {
        STATUS: resposta.status_code,
        JSON: resposta.json(),
        VAR: len(resposta.json()),
    }


@when("verify_size_list")
def step_when_verify(context):
    context.response[GET_ALL][VAR] = len(context.response[GET_ALL][JSON])


@when("not_empty_list")
def step_when_not_empty_list(context):
    if context.response[GET_ALL][VAR] == 0:
        context.session.post(
            f"{API_URL}/incidents", headers=AUTH, json=generate_post_random_data()
        )

        resposta = context.session.get(f"{API_URL}/incidents", headers=AUTH)
        assert resposta.status_code == 200
        context.response = {
            GET_ALL: {
                STATUS: resposta.status_code,
                JSON: resposta.json(),
                VAR: len(resposta.json()),
            }
        }


@when("empty_list")
def step_when_empty_list(context):
    if context.response[GET_ALL][VAR] > 0:
        for item in context.response[GET_ALL][JSON]:
            id = item["id"]
            context.session.delete(f"{API_URL}/incidents/{id}", headers=AUTH)

        resposta = context.session.get(f"{API_URL}/incidents", headers=AUTH)
        assert resposta.status_code == 200
        context.response = {
            GET_ALL: {
                STATUS: resposta.status_code,
                JSON: resposta.json(),
                VAR: len(resposta.json()),
            }
        }


@when("view_created_incident_details")
def step_when_created_details(context):
    incident_id = context.response[SAVE][JSON]["id"]
    resposta = context.session.get(f"{API_URL}/incidents/{incident_id}", headers=AUTH)
    assert resposta.status_code == 200
    context.response[GET_ONE] = {
        STATUS: resposta.status_code,
        JSON: resposta.json(),
        VAR: incident_id,
    }


@when("view_updated_incident_details")
def step_when_updated_details(context):
    incident_id = context.response[SAVE][JSON]["id"]
    resposta = context.session.get(f"{API_URL}/incidents/{incident_id}", headers=AUTH)
    assert resposta.status_code == 200
    context.response[GET_ONE] = {
        STATUS: resposta.status_code,
        JSON: resposta.json(),
        VAR: incident_id,
    }


@when("view_incident_details")
def step_when_view_incident(context):
    list_incident = context.response[GET_ALL][JSON]
    random_incident_id = random.choice(list_incident)["id"]
    resposta = context.session.get(
        f"{API_URL}/incidents/{random_incident_id}", headers=AUTH
    )
    assert resposta.status_code == 200
    context.response[GET_ONE] = {
        STATUS: resposta.status_code,
        JSON: resposta.json(),
        VAR: random_incident_id,
    }


@when("view_inexistent_incident")
def step_when_view_incident(context):
    incident_id = "teste"
    resposta = context.session.get(f"{API_URL}/incidents/{incident_id}", headers=AUTH)
    assert resposta.status_code == 500
    context.response[ERROR] = {STATUS: resposta.status_code}


@when("delete_a_incident_from_list")
def step_when_delete_from_list(context):
    list_incident = context.response[GET_ALL][JSON]
    random_incident_id = random.choice(list_incident)["id"]
    resposta = context.session.delete(
        f"{API_URL}/incidents/{random_incident_id}", headers=AUTH
    )
    assert resposta.status_code == 200
    context.response[DELETE] = {
        STATUS: resposta.status_code,
        JSON: resposta.json(),
        VAR: random_incident_id,
    }


@when("delete_this_incident")
def step_when_delete_this_incident(context):
    incident_id = context.response[GET_ONE][JSON]["id"]
    resposta = context.session.delete(
        f"{API_URL}/incidents/{incident_id}", headers=AUTH
    )
    assert resposta.status_code == 200
    context.response[DELETE] = {
        STATUS: resposta.status_code,
        JSON: resposta.json(),
        VAR: incident_id,
    }


@when("delete_inexistent_incident")
def step_when_error_delete(context):
    incident_id = "teste"
    resposta = context.session.delete(
        f"{API_URL}/incidents/{incident_id}", headers=AUTH
    )
    assert resposta.status_code == 500
    context.response[ERROR] = {STATUS: resposta.status_code}


@when("create_new_incident")
def step_when_create(context):
    data = generate_post_random_data()

    resposta = context.session.post(f"{API_URL}/incidents", headers=AUTH, json=data)
    assert resposta.status_code == 200
    context.response[SAVE] = {
        STATUS: resposta.status_code,
        JSON: resposta.json(),
        VAR: data["name"],
    }


@when("create_incident_with_invalid_parameters")
def step_when_error_create(context):
    data = generate_post_random_data_error()

    resposta = context.session.post(f"{API_URL}/incidents", headers=AUTH, json=data)
    assert resposta.status_code == 500
    context.response[SAVE] = {
        STATUS: resposta.status_code,
        JSON: resposta.json(),
        VAR: data["name"],
    }


@when("update_an_incident")
def step_when_update(context):
    incident_id = context.response[GET_ONE][JSON]["id"]
    data = generate_put_random_data()

    resposta = context.session.put(
        f"{API_URL}/incidents/{incident_id}", headers=AUTH, json=data
    )
    assert resposta.status_code == 200
    context.response[SAVE] = {
        STATUS: resposta.status_code,
        JSON: resposta.json(),
        VAR: data["name"],
    }


@when("update_incident_with_invalid_parameters")
def step_when_error_update(context):
    incident_id = context.response[GET_ONE][JSON]["id"]
    data = generate_put_random_data_error()

    resposta = context.session.put(
        f"{API_URL}/incidents/{incident_id}", headers=AUTH, json=data
    )
    assert resposta.status_code == 500
    context.response[SAVE] = {
        STATUS: resposta.status_code,
        JSON: resposta.json(),
        VAR: data["name"],
    }


@when("update_inexistent_incident")
def step_when_error_update_not_found(context):
    incident_id = "teste"
    data = generate_put_random_data()

    resposta = context.session.put(
        f"{API_URL}/incidents/{incident_id}", headers=AUTH, json=data
    )
    assert resposta.status_code == 500
    context.response[ERROR] = {STATUS: resposta.status_code}


@then("verifyNotEmptyList")
def step_then_not_empty_list(context):
    assert context.response[GET_ALL][VAR] != 0


@then("verifyEmptyList")
def step_then_not_empty_list(context):
    assert context.response[GET_ALL][VAR] == 0


@then("incidentActiveSuccess")
def step_then_incident_success(context):
    assert context.response[GET_ONE][STATUS] == 200
    assert context.response[GET_ONE][JSON]["id"] == context.response[GET_ONE][VAR]


@then("deleteSuccess")
def step_then_delete_success(context):
    assert context.response[DELETE][STATUS] == 200
    assert context.response[DELETE][JSON]["id"] == context.response[DELETE][VAR]


@then("creationSuccess")
def step_then_creation_success(context):
    assert context.response[SAVE][STATUS] == 200
    assert context.response[SAVE][JSON]["name"] == context.response[SAVE][VAR]


@then("updateSuccess")
def step_then_update_success(context):
    assert context.response[SAVE][STATUS] == 200
    assert context.response[SAVE][JSON]["name"] == context.response[SAVE][VAR]


@then("errorCreateIncident")
def step_then_error_create(context):
    assert context.response[SAVE][STATUS] == 500


@then("errorUpdateIncident")
def step_then_error_update(context):
    assert context.response[SAVE][STATUS] == 500


@then("notFoundIncident")
def step_then_incident_not_found(context):
    assert context.response[ERROR][STATUS] == 500
