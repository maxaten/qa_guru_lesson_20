from jsonschema.validators import validate
from tests_api.helper import load_json_schema, reqres_session


def test_page_number_validation_schema_200():
    page = 2
    schema = load_json_schema('get_page_number.json')

    response = reqres_session.get(url='/api/users', params={'page': page})

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 200
    assert response.json()['page'] == page


def test_users_list_def_length_validation_schema_200():
    default_users_count = 6
    schema = load_json_schema('get_user_list.json')

    response = reqres_session.get(url='/api/users')

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 200
    assert len(response.json()['data']) == default_users_count


def test_user_not_found_404():
    response = reqres_session.get(url='/api/users/23')

    print(response.text)
    assert response.status_code == 404
    assert response.text == '{}'


def test_create_user_validation_schema_201():
    name = 'Olga'
    job = 'Manager'
    schema = load_json_schema('post_create_user.json')

    response = reqres_session.post(
        url='/api/users',
        json={
            'name': name,
            'job': job
        })

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 201
    assert response.json()['name'] == name
    assert response.json()['job'] == job


def test_delete_users_204():
    response = reqres_session.delete(url='/api/users/2')

    assert response.status_code == 204
    assert response.text == ''


def test_patch_user_validation_schema_200():
    name = 'morpheus'
    job = 'zion resident'
    schema = load_json_schema('patch_user.json')

    response = reqres_session.patch(
        url='/api/users/2',
        json={
            "name": name,
            "job": job
        }
    )

    validate(response.json(), schema=schema)
    assert response.status_code == 200
    assert response.json()['name'] == name
    assert response.json()['job'] == job


def test_update_user_validation_schema_200():
    name = 'Ololosha'
    job = 'President'
    schema = load_json_schema('put_update_user.json')

    response = reqres_session.put(
        url='/api/users/2',
        json={
            "name": name,
            "job": job
        }
    )

    validate(response.json(), schema=schema)
    assert response.status_code == 200
    assert response.json()['name'] == name
    assert response.json()['job'] == job


def test_login_user_validation_schema_200():
    email = 'eve.holt@reqres.in'
    password = 'cityslicka'
    schema = load_json_schema('post_login_user.json')

    response = reqres_session.post(
        url='/api/login',
        json={
            "email": email,
            "password": password
        }
    )

    validate(response.json(), schema=schema)
    assert response.status_code == 200


def test_user_login_unsuccessful_validation_schema_400():
    email = 'peter@klaven'
    text_error = 'Missing password'
    schema = load_json_schema('post_user_login_unsuccessful.json')

    response = reqres_session.post(
        url='/api/login',
        json={
            'email': email
        }
    )

    validate(response.json(), schema=schema)
    assert response.status_code == 400
    assert response.json()['error'] == text_error


def test_register_user_validation_schema_200():
    email = 'eve.holt@reqres.in'
    password = 'pistol'
    schema = load_json_schema('post_register_user.json')

    response = reqres_session.post(
        url='/api/register',
        json={
            "email": email,
            "password": password
        }
    )

    validate(response.json(), schema=schema)
    assert response.status_code == 200


def test_register_unsuccessful_user_validation_schema_400():
    email = 'sydney@fife'
    text_error = 'Missing password'
    schema = load_json_schema('post_unregister_user.json')

    response = reqres_session.post(
        url='/api/register',
        json={
            "email": email
        }
    )

    validate(response.json(), schema=schema)
    assert response.status_code == 400
    assert response.json()['error'] == text_error


def test_delayed_response_validation_schema_200():
    delay = 3
    per_page = 6
    page = 1
    schema = load_json_schema('get_delay_response.json')

    response = reqres_session.get(
        url='/api/users',
        params={'delay': delay}
    )

    validate(response.json(), schema=schema)
    assert response.status_code == 200
    assert response.json()['per_page'] == per_page
    assert response.json()['page'] == page


