from functools import cached_property

import requests
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import ConnectionError

from main.service.exceptions import (BrapiConnectionError, BrapiException,
                                     BrapiTimeoutException,
                                     BrapiTooManyRequestsError)


class ResponseWrapper:
    def __init__(self, request, response):
        self.request = request
        self.response = response

    @cached_property
    def raw(self):
        return self.response.json()

    @cached_property
    def cleaned(self):
        return self.request.clean_response(self.raw)

    @cached_property
    def parsed(self):
        return self.request.parse_response(self.cleaned)


class BaseRequest:
    extra_logs = {'api': 'BrapiAPI', 'log_type': 'request_log'}

    def __init__(self, client: dict):
        self.client = client
        self.session = self._build_session()

    def _build_session(self):
        session = requests.Session()
        retry_strategy = Retry(total=3, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        return session

    def send(self, params: dict = None, json: dict = None):
        response = self._request(self.method, self.endpoint, params=params, json=json)
        return ResponseWrapper(self, response)

    def _request(self, method: str, endpoint: str, params: dict, json: dict):
        url = f"{self.client['base_url']}/{endpoint}"
        try:
            response = self.session.request(method, url, params=params, json=json)
        except ConnectionError as e:
            msg = f"brapi '{method} {url}' json={json} params={params} connection error"
            self.client['logger'].info(msg, extra=self.extra_logs)
            raise BrapiConnectionError(msg) from e

        msg = (
            f"brapi '{method} {url}' json={json} params={params} status_code={response.status_code}"
        )
        if response.ok:
            self.client['logger'].info(msg, extra=self.extra_logs)
        elif response.status_code == 429:
            raise BrapiTooManyRequestsError(msg)
        elif response.status_code == 408:
            raise BrapiTimeoutException(msg)
        else:
            raise BrapiException(msg)

        return response
