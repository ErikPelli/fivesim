from ast import Call
import requests
from typing import Any, Callable, NamedTuple


class _APIResult(NamedTuple):
    '''A tuple with the HTTP Status Code and the Body of the Response'''
    status_code: int
    body: str


class _APIRequest:
    def __init__(self, endpoint: str, auth_token: str):
        self.__endpoint = endpoint
        self.__authentication_token = auth_token

    def __request(self, method: Callable[[Any], requests.Response], name: str, use_token: bool) -> requests.Response:
        headers = {"Accept": "application/json"}
        if use_token:
            headers["Authorization"] = "Bearer " + self.__authentication_token
        return method(url=self.__endpoint + name, headers=headers)

    def _GET(self, use_token: bool, path: str) -> _APIResult:
        """
        Make a GET request to the API.

        :param use_token: Specify wheter to include the authentication token in the request
        :param path: Specify the part after the domain to invoke in the API
        """
        result = self.__request(method=requests.get,
                                name=path, use_token=use_token)
        return _APIResult(status_code=result.status_code, body=result.text)

    def _POST(self, use_token: bool, path: str) -> _APIResult:
        """
        Make a POST request to the API.

        :param use_token: Specify wheter to include the authentication token in the request
        :param path: Specify the part after the domain to invoke in the API
        :return: A tuple with the HTTP Status Code and the Body of the Response
        """
        result = self.__request(method=requests.post,
                                name=path, use_token=use_token)
        return _APIResult(status_code=result.status_code, body=result.text)
