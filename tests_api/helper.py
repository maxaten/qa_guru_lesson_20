import json
import logging
import os.path

import allure
import curlify
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from requests import Session, Response


def load_json_schema(name: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    schemas_dir = os.path.join(script_dir, '..', 'schemas')
    schema_path = os.path.join(schemas_dir, name)
    with open(schema_path) as schema:
        return json.loads(schema.read())


class CustomSession(Session):
    def __init__(self, base_url):
        self.base_url = base_url
        super().__init__()

    def request(self, method, url, *args, **kwargs) -> Response:
        response = super(CustomSession, self).request(method=method, url=self.base_url + url, *args, **kwargs)
        curl = curlify.to_curl(response.request)
        status_code = response.status_code
        logging.info(f'status code:{status_code}\n{curl}')
        with step(f'{method} {url}'):
            allure.attach(body=f'status code:{status_code}\n{curl}', name='Request curl',
                          attachment_type=AttachmentType.TEXT, extension='txt')

            try:
                response_body = response.json()
            except json.JSONDecodeError:
                response_body = response.text

        allure.attach(body=json.dumps(response_body, indent=2), name='Response body',
                      attachment_type=AttachmentType.JSON)
        return response


base_url = 'https://reqres.in'

reqres_session = CustomSession(base_url)
