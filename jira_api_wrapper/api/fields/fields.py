from jira_api_wrapper.api.base_api import BaseApi


class JiraFields(BaseApi):
    def __init__(self, host, user, token):
        super().__init__(host, user, token)

    def get_fields(self):
        response = self.session.get(
            self.endpoint['get_fields']
        )
        return self.parse_response(response)

    def get_all_issue_field_options(self, field_key):
        response = self.session.get(
            self.set_path_params(
                self.endpoint['get_all_issue_field_options'],
                field_key
            )
        )
        return self.parse_response(response)
