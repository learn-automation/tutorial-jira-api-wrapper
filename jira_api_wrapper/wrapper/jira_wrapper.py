import os

from jira_api_wrapper.api.fields.fields import JiraFields

class JiraWrapper(JiraFields):
    def __init__(self, host, user, token):
        super().__init__(host, user, token)


a = JiraWrapper('http://learn-automation.atlassian.net', 'jonathoncarlyon@gmail.com', os.environ('JIRA_TOKEN'))
print(
    a.set_path_params(
        a.endpoint['get_issue_field_option'],
        'boo',
        'who'
    )
)
#c = a.get_all_issue_field_options('customfield_10002')
#b = 'foo'