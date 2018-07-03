class JiraEndpoints:
    def __init__(self, host):
        api = f'{host}/rest/api/2'
        self.endpoint = {
            # Myself
            'get_current_user': f'{api}/myself',
            # Fields
            'get_fields':
                f'{api}/field',
            'create_custom_field':
                f'{api}/field',
            'get_all_issue_field_options':
                f'{api}/field/{{}}/option',
            'create_issue_field_option':
                f'{api}/field/{{}}/option',
            'get_issue_field_option':
                f'{api}/field/{{}}/option/{{}}',
            'update_issue_field_option':
                f'{api}/field/{{}}/option/{{}}',
            'delete_issue_field_option':
                f'{api}/field/{{}}/option/{{}}',
            'replace_issue_field_option':
                f'{api}/field/{{}}/option/{{}}/issue',
            'get_selectable_issue_field_options':
                f'{api}/field/{{}}/option/suggestions/edit',
            'get_visible_issue_field_options':
                f'{api}/field/{{}}/option/suggestions/search',
        }
