from errors import InvalidAPIKeyError, BadRequestError
import requests
from typing import Any, Callable, Dict, NamedTuple


class _APIResult(NamedTuple):
    '''A tuple with the HTTP Status Code and the Body of the Response'''
    status_code: int
    status_description: str
    body: str


class _APIRequest:
    def __init__(self, endpoint: str, auth_token: str) -> None:
        self.__endpoint = endpoint
        self.__authentication_token = auth_token

    def __request(self, method: Callable[[Any], requests.Response], name: str, use_token: bool, params: dict) -> requests.Response:
        headers = {"Accept": "application/json"}
        if use_token:
            headers["Authorization"] = "Bearer " + self.__authentication_token
        return method(url=self.__endpoint + name, headers=headers, params=params)

    def _GET(self, use_token: bool, path: str, parameters: Dict[str, str]) -> _APIResult:
        """
        Make a GET request to the API.

        :param use_token: Specify wheter to include the authentication token in the request
        :param path: Specify the part after the domain to invoke in the API
        """
        result = self.__request(
            method=requests.get,
            name=path,
            use_token=use_token,
            params=parameters
        )
        return _APIResult(status_code=result.status_code, body=result.text, status_description=result.reason)

    def _POST(self, use_token: bool, path: str, parameters: Dict[str, str]) -> _APIResult:
        """
        Make a POST request to the API.

        :param use_token: Specify wheter to include the authentication token in the request
        :param path: Specify the part after the domain to invoke in the API
        :return: A tuple with the HTTP Status Code and the Body of the Response
        """
        result = self.__request(
            method=requests.post,
            name=path,
            use_token=use_token,
            params=parameters
        )
        return _APIResult(status_code=result.status_code, body=result.text)

    @staticmethod
    def _check_error(result: _APIResult) -> None:
        """
        Check if the API request was successful.

        :raises FiveSimError: if there is an error with the request
        """
        if result.status_code == 401:
            raise InvalidAPIKeyError
        if result.status_code == 400:
            raise BadRequestError(result.status_description)
