import pytest

def test_exception_exists_NotEligibleForPathParams():
    from jira_api_wrapper.api.exceptions import NotEligibleForPathParams
    assert NotEligibleForPathParams


def test_exception_exists_NotEligibleForPathParams():
    from jira_api_wrapper.api.exceptions import NotEligibleForPathParams
    assert '{}' in NotEligibleForPathParams.__doc__
