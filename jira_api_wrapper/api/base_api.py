import requests

from jira_api_wrapper.api.exceptions import *
from jira_api_wrapper.api.endpoints import JiraEndpoints


class BaseApi(JiraEndpoints):
    """ Base class to be consumed in all API classes """
    def __init__(self, host, user, token):
        super().__init__(host)
        self.session = requests.Session()
        self.session.auth = (user, token)

    @staticmethod
    def parse_response(response):
        response.raise_for_status()
        return response.json()

    @staticmethod
    def set_path_params(endpoint, *args):
        if '{}' in endpoint:
            return endpoint.format(*args)
        else:
            raise NotEligibleForPathParams(
                NotEligibleForPathParams.__doc__.format(endpoint)
            )
