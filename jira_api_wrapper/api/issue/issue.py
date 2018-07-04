from jira_api_wrapper.api.base_api import BaseApi


class JiraIssue(BaseApi):
    def __init__(self, host, user, token):
        super().__init__(host, user, token)

    def get_issue(self, issue_id_or_key):
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/#api-api-2-issue-issueIdOrKey-get
        GET /rest/api/2/issue/{issueIdOrKey}
        Returns a full representation of the issue for the given issue key.
        The issue JSON consists of the issue key and a collection of fields. Additional information like links to workflow transition sub-resources, or HTML rendered values of the fields supporting HTML rendering can be retrieved with expand request parameter specified.
        The fields request parameter accepts a comma-separated list of fields to include in the response. It can be used to retrieve a subset of fields. By default all fields are returned in the response. A particular field can be excluded from the response if prefixed with a “-” (minus) sign. Parameter can be provided multiple times on a single request.
        By default, all fields are returned in the response. Note: this is different from a JQL search - only navigable fields are returned by default (*navigable).
        App scope required: READ
        Response content type: application/json
        :param issue_id_or_key: String containing the Jira issue id or key
        :return: Dict containing API response.
        """
        response = self.session.get(
            self.set_path_params(
                self.endpoint['get_issue'],
                issue_id_or_key
            )
        )
        return self.parse_response(response)
