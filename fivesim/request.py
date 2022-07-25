import json
import requests
from fivesim.errors import BadRequestError, InvalidAPIKeyError, InvalidResultError
from typing import Any, Callable, Dict, NamedTuple

from fivesim.fivesim import FiveSim


class _APIResult(NamedTuple):
    '''A tuple with the HTTP Status Code and the Body of the Response'''
    status_code: int
    status_description: str
    body: str


class _APIRequest:
    def __init__(self, endpoint: str, auth_token: str) -> None:
        self.__endpoint = endpoint
        self.__authentication_token = auth_token

    def __request(self, method: Callable[[Any], requests.Response], name: str, use_token: bool, params: dict, json_data: str) -> requests.Response:
        headers = {"Accept": "application/json"}
        if use_token:
            headers["Authorization"] = "Bearer " + self.__authentication_token
        response = method(
            url=self.__endpoint + name,
            headers=headers,
            params=params,
            data=json_data
        )
        if response.status_code == 401:
            raise InvalidAPIKeyError
        elif response.status_code == 400:
            raise BadRequestError(response.reason)
        elif response.status_code != 200:
            raise FiveSim(response.reason)
        else:
            return response

    def _GET(self, use_token: bool, path: str, parameters: Dict[str, str] = {}, data: Dict[str, str] = None) -> _APIResult:
        """
        Make a GET request to the API.

        :param use_token: Specify wheter to include the authentication token in the request
        :param path: Specify the part after the domain to invoke in the API
        :return: An object with the response values
        :raises FiveSimError: if there is an error with the request
        """
        result = self.__request(
            method=requests.get,
            name=path,
            use_token=use_token,
            params=parameters,
            json_data=json.dumps(data) if data is not None else None
        )
        return _APIResult(status_code=result.status_code, body=result.text, status_description=result.reason)

    def _POST(self, use_token: bool, path: str, parameters: Dict[str, str] = {}) -> _APIResult:
        """
        Make a POST request to the API.

        :param use_token: Specify wheter to include the authentication token in the request
        :param path: Specify the part after the domain to invoke in the API
        :return: An object with the response values
        :raises FiveSimError: if there is an error with the request
        """
        result = self.__request(
            method=requests.post,
            name=path,
            use_token=use_token,
            params=parameters,
            json_data=None
        )
        return _APIResult(status_code=result.status_code, body=result.text)

    @classmethod
    def _parse_json(cls, input: str, need_keys: list[str] = [], into_object: Callable[[dict], Any] = None) -> Dict:
        """
        Parse JSON into a generic dictionary.

        :param input: JSON data
        :return: Parsed dictionary
        :raises InvalidResultError: when the requested keys aren't in the output
        """
        try:
            result = json.loads(input, object_hook=into_object)
        except:
            result = {}

        for key in need_keys:
            if not key in result:
                raise InvalidResultError(input)

        return result
