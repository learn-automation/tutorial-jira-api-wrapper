Jira API Wrapper Tutorial
===
This tutorial should teach you how to build a light-weight API wrapper for [Jira](https://www.atlassian.com/software/jira).

Getting Started
---
#### Prerequisites
    1. Python3.6+ is installed
    2. You have access to a Jira Cloud instance 
        1. If you do not have access to Jira, please email [Jonny](slack://user?team={TBGGJGQAY}&id={UBG77CB25})
#### First steps
1. Log into Jira and generate a personal API token
    1. Navigate to [https://id.atlassian.com/manage/api-tokens](https://id.atlassian.com/manage/api-tokens)
    2. Click Create API Token
        1. Save token value somewhere safe
2. Create new Python project for the Jira API wrapper, mine will be named "jira-api-wrapper"
    1.  The project structure should look similar to this:
    ```
    jira-api-wrapper
    ├── jira_api_wrapper/
    │   ├── api/
    │   │   ├── fields/
    │   │   │   ├── fields.py   
    │   │   ├── issue/
    │   │   │   ├── issue.py            
    │   │   ├── exceptions.py
    │   │   ├── endpoints.py
    │   │   ├── wrapper.py
    │   ├── wrapper/
    │   │   ├── jira_wrapper.py
    ├── test/
    │   ├── test_api/
    │   │   ├── test_fields/
    │   │   │   ├── test_fields.py
    │   │   ├── test_issue/
    │   │   │   ├── test_issue.py
    │   │   ├── test_wrapper.py
    │   ├── test_jira_wrapper/
    │   │   ├── test_jira_wrapper.py
    ├── etc/
    │   ├── version.txt
    │   ├── .bumpversion.cfg
    │   ├── .pylintrc
    ├── setup.py
    ├── README.md
    └──  
    ```
    Note: Creating a good readme is important, please use [this](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) as a template.
3. Since we already know how our project is going to be laid out we can create [setup.py](#create-setuppy).
4. Now we are ready to define the URLs to the endpoints by creating [jira_api_wrapper/api/endpoints.py](#create-endpointspy).  
I have provided an example for only two endpoints.
To extend the functionality of this wrapper to include additional endpoints, you can add them using by using the [JIRA Cloud REST API documentation](https://developer.atlassian.com/cloud/jira/platform/rest/#api-api-2-application-properties-get).
I use the endpoint name as the dictionary key, and the path to the endpoint as the value.  
If the endpoint uses path parameters we need to replace it with a placeholder. 
This endpoint `Set application property  /rest/api/2/application-properties/{id}` would be written as `'set_application_property': f'{api}/application-properties/{{}}'`
5. Some endpoints will use path parameters (`/rest/api/2/issue/{issueIdOrKey}/assignee`) while others do not (`/rest/api/2/field`).
One scenario that quickly comes to mind is "What happens when a user tries to set a path parameter when it doesn't take one?".
To accommodate for this scenario we can create a custom exception to make it very clear to the user if they are 
attempting to set path parameters on an endpoint that does not accept them.
To do this we must create [jira_api_wrapper/api/exceptions.py](#create-exceptionspy).
6. At this point we have what we need to create [jira_api_wrapper/api/base_api.py](#create-base-apipy).  
This provides us with a base class that will be inherited by the classes that interact with the API in the next steps.  
7. Finally we get to actually interact with the API by creating [jira_api_wrapper/api/fields/fields.py](#create-fieldspy).  
All the logic for interacting with the `/rest/api/2/issue/*` endpoint should be contained within this class.
8. Let's add another endpoint just as we did in the previous step by creating [issue.py](#create-issuepy).
9. To help us easily manage our imports, we will create [jira_api_wrapper/api/__init\__.py](#create-api__init__py)
10. It is time to add the actual wrapper that will be exposed to the user by creating [jira_api_wrapper/wrapper/jira_wrapper.py](#create-jira_wrapperpy).  
This class, `JiraWrapper`, will inherit from all the API classes (such as `JiraFields` and `JiraIssue`) which means `JiraWrapper` now contains all the methods as the parent class, such as `.get_fields()` and `.get_issue()`
11. In the current state of this project, after a user installs this wrapper, importing it feel strange.  
To fix this we will create [jira_api_wrapper/__init\__.py](#create-jira_api_wrapper__init__py).  
Now we can do:  
`from jira_api_wrapper import JiraWrapper`  
Instead of:   
`from jira_api_wrapper.wrapper.jira_wrapper import JiraWrapper`    


### Code Explanations
#### Create setup.py
 1. ##### What is setup.py?
     Unfortunately the correct answer has more complexity than this [Stackoverflow answer](https://stackoverflow.com/a/1472014/1834048):
     >setup.py is a python file, which usually tells you that the module/package you are about to install has been packaged and distributed with Distutils, which is the standard for distributing Python Modules.\
     This allows you to easily install Python packages. Often it's enough to write:\
     `$ python setup.py install`\
     and the module will install itself.
     
     While the above is true, it does not speak about Setuptools. 
     Setuptools was created due to limitations presented by Distutils (such as not being easily able to package/consume non-python files within a module).  
     One issue is that Setuptools monkeypatches (redefines functionality) Distutils under the hood which created a bit of chaos.  
     This becomes especially confusing when the functionality of the Python package you produce changes greatly just from the import you picked in setup.py: 
     `from setuptools import setup` vs `from distutils import setup` 
     
     Things get even worse when we bring pip into the mix.  Pip is the standard Python package manager.  Pip uses setuptools, but it's distutils that's built into Python, not setuptools.  
     
     For all these reasons and more, I ask everyone:  Please help end this madness.  Start using Pip and Setuptools for everything, instead of the old distutils way.  
     ##### Use the following:
     * Use `from setuptools import setup`
     * `pip install -e .[dev]` instead of `python setup.py develop`
     * `pip install -e .[dev]` instead of `pip install -r requirements.txt`
     * `pip install .` instead of `python setup.py install`
 
 2. ##### What should setup.py look like?
     ```python
    from setuptools import setup
    
    with open('etc/version.txt') as file:
        version = file.read().strip()
 
    requirements = [
        'requests>=2.18.4'
    ]
 
    dev_requirements = [
          'pytest>=3.5.1'
    ] 
 
    setup(name='jira_api_wrapper',
          version=version,
          description='Configuration driven web scraping framework',
          author='Jonathon Carlyon',
          author_email='JonathonCarlyon@gmail.com',
          url='https://github.com/JonnyFb421/scrapeit',
          install_requires=requirements,
          extras_require={'dev': dev_requirements},
          packages=['jira_api_wrapper', 
                    'jira_api_wrapper.api', 
                    wrapper],
    )
      ```
 3. ##### How do I use setup.py?
     1. How application should use it: `pip install .`
     2. How developers should use it: `pip install -e .[dev]`
     3. How Jenkins (or other CI systems) should use it: `pip install .[dev]`
     
     Note: `.` can be substituted for a path to the directory where setup.py lives.  
     The `-e` flag used here means "editable" so the module will be loaded from your local workspace instead of the module being installed to site-packages: `/usr/local/lib/python3.6/dist-packages`
       
 4. ##### What about requirements.txt?
     Do away with it.  Setup.py can contain the application runtime dependencies (set from the `install_requires` attribute) as well as extra dependency sets (set from the `extras_require` attribute).  
     Using the `setup.py` example above, `pip install .[dev]` would install the requests module (my runtime dependency) and pytest (my testing dependency)
     
 5. ##### Other helpful setup.py tips:
     1. Use `pip show <module>` to see what version of a module you're using

#### Create endpoints.py
 1. ##### What is endpoints.py?
     This file is simply to define all the endpoints we want our wrapper to be capable of hitting.  You will need to consult the [API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/) to see the full list of endpoints.  
     
 2. ##### What should endpoints.py look like?
     ```python
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
    ```
 3. ##### What is endpoints.py doing, and why is it so ugly?
     We are creating a class here to contain all the JiraEndpoints.  The class only has one attribute: `endpoint`. Endpoint is a dictionary that contains the Jira endpoint's name as the dictionary key, and the URL as the dictionary value.  
     Python3.6 introduced [f-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings) which makes string interpolation a lot cleaner since you can now specify the variable within curly braces.  
     ```
     my_var='hello'
     print(f'{my_var} world')
     > hello world" 
     ```
     In some of the URLs above you can see string values like: 
     `f'{api}/field/{{}}/option'` 
     
     When this gets evaluated, Python will substitute {api} with the value of that variable.  
     The double brackets (between field and option) are how you escape curly brackets within an f-string.
     This is particularly useful since you can still call the old string interpolation method on strings that contain empty curly brackets by using `"{} world.format(my_var)`.
     This will be needed in order to pass variables back into the path since [REST design](https://stackoverflow.com/a/31261026/1834048) "is that path params are used to identify a specific resource or resources, while query parameters are used to sort/filter those resources."
     
     Note: This does not have to be a class, and some would argue that it shouldn't be it's own class since it's only setting a dictionary, but I think it is better organized when lumped into a class and inherited by the wrapper
 4. ##### How to use endpoints.py
     The class inside the endpoints module, JiraEndpoints, will be used as the base class for our base API class. 
     
 5. ##### What about tests?
    Although it is a slipperly slope to get into this mentality, I do not think tests are required for this class.
    There is no logic, it just sets a dictionary containing static set of URLs with placeholders.  
    It's possible to write tests to assert that certain endpoints exist inside this dictionary, but this will be covered when we run the tests on the child classes. 
     
#### Create exceptions.py
 1. ##### What is exceptions.py?
     This module contains all of the custom exceptions that our API is going to throw.
     This becomes powerful since you can use try/except blocks when calling your wrapper while catching
     for your custom exceptions instead of broader HTTP exceptions.
     
 2. ##### What should exceptions.py look like?
     ```python
    class NotEligibleForPathParams(Exception):
        """ The following endpoint: {} is not eligible to use path parameters """
     ```
     
 3. ##### What's going on here?
     We are defining a new class, `NotEligibleForPathParams`, and inheriting the Exception class.
     The definition of these exception classes don't need any logic and often contain only `pass`. 
     Instead of using `pass`, I like to use docstrings (a docstring is the value encapsulated in triple quotes).
     When using a docstring we are actually setting a special attribute of the class, `__doc__`.
     I like to take advantage of this by defining the error message I want the exception to raise as a docstring.  
     I also leave a placeholder in the docstring so we can call `NotEligibleForPathParams.__doc__.format(endpoint)`
     which will return:  
     `The following endpoint: http://example.com/rest/api/2/myself is not eligible to use path parameters`
     
 4. ##### What about tests?
    We can add an extremely simple tests for this.  
    Create `tests/test_api/test_exceptions.py`
    ```python
    import pytest
    
    def test_exception_exists_NotEligibleForPathParams():
        from jira_api_wrapper.api.exceptions import NotEligibleForPathParams
        assert NotEligibleForPathParams
    ```
    We are using pytest to create and run our tests, so the first step to writing a test is importing pytest.  
    For pytest to run this test, a couple conditions need to be hit:  
        1. The test file lives in a directory that starts with test_*  
        2. The test method begins with test_*  
    When writing test method names do not be afraid to break [Pep 8 (the official python style guide)](https://www.python.org/dev/peps/pep-0008/?#function-and-variable-names)
    conventions as long as it makes sense. 
    In my example above, I have violated the function name convention by naming my test function with snake case with title case,
    but it was done to increase readability of what this test is actually doing.  
    Now we can talk about what is going on inside of this test.
        1. We import the exception class NotEligibleForPathParams
        2. We call `assert NotEligibleForPathParams` which would fail the test if `NotEligibleForPathParams` was None.  
        This is how we can verify the exception exists.
   
    Let's add one more test to be sure that the placeholder exists in the doc string, because if someone unknowingly removes the placeholder, we will get an exception when calling `.format()` on the docstring elsewhere in the code.
    ```python
    def test_placeholder_exists_in_NotEligibleForPathParams_docstring():
        from jira_api_wrapper.api.exceptions import NotEligibleForPathParams
        assert '{}' in NotEligibleForPathParams.__doc__
    ```    
    This test will help us ensure we don't unknowingly remove code that will break something else.
    
#### Create base_api.py
 1. ##### What is base_api.py?
     This module will contain the base class that all API classes inherit from.  
     Any logic that we want to be in every API class should live here.  
     
 2. ##### What should base_api.py?
     ```python
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
     ```
 3. ##### What is base_api.py doing
     1. `class BaseApi(JiraEndpoints)` We are defining a class BaseAPI and inheriting JiraEndpionts.
     2. `def __init__(self, host, user, token):` We are stating that this class requires three parameters to initialize: `host, user, token`
     3. `super().__init__(host)` We are using `super()` to run the `__init__()` method of the parent class (JiraEndpoints) which requires a `host` argument. 
     In this case, the `__init__()` method of the parent class sets the `self.endpoint` dictionary.
     4. `self.session = requests.Session()` calling `requests.Session()` will return a Session object.
     A Session object is basically a wrapper for `requests` that allows you to persist data.
     5. `self.session.auth = (user, token)` this will attach a [HTTP Header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) for authorization with every request.
     That means when we call `self.session.get('http://my-domain.com')` we will be implicitly passing a header that looks like this: `Authorization: user:token`
     6. `@staticmethod` The static method decorator means that the method below does not have access to the rest of the class, and does not need `self` as the first parameter.
     7. `response.raise_for_status()` The `requests.Response` object contains some really handy built-in methods.
     This method will raise an exception if an HTTP error has occurred.
     It's important to note that the `requests` module will catch HTTP errors and store them into the response object.
     If you're not careful, you may get a bad response and unknowingly access the json. 
     In this scenario, Python will throw an exception complaining that you're trying to access something that does not exist, which may be confusing when the reality is just that you got a bad response back from the server you sent a request to. 
     8. `return response.json()` Now that we know the response was good (we checked using `.raise_for_status()`), we are safe to return the json of the response object using the `.json()` method
     9. `def set_path_params(endpoint, *args)` Here we are using [*args](https://stackoverflow.com/a/3394898/1834048) which allows flexibility around how many arguments are passed to this method.
     Since we are setting path parameters which may vary depending on API endpoint, the use of `*args` is appropriate.
     Make note: `*args` should only be used when you have cases like this, where you know you are going to be passing a different amount of arguments.
     The Python community places a high value on [**Explicit is better than implicit**](Explicit is better than implicit.).  
     10. `if '{}' in endpoint:` Here we are checking if the string literal `"{}"` appears in the url for the endpoint.
     11. `return endpoint.format(*args)` If the placeholders (`"{}"`) were found in the string, use the `.format()` method and pass in `*args`.
     12. ` raise NotEligibleForPathParams(NotEligibleForPathParams.__doc__.format(endpoint))`
     We are raising a custom exception, then using the exception's docstring as it's error message.
     The docstring for the exception has a placeholder (`"{}"`) in it, so again we can call `.format()` and pass in the relevant data (the url to the endpoint in this case).
     
#### Create fields.py
 1. ##### What is fields.py?
     This module is responsible for holding all the logic for the `fields` endpoints.
     
 2. ##### What should fields.py look like?
     ```python
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
     ```
 3. ##### What is fields.py doing?
     1. `class JiraFields(BaseApi):` We are creating a new class and inheriting from the BaseApi class
     2. `def __init__(self, host, user, token):` We are defining our `__init__` method, 
     and requiring `host, user, token` to be passed in when initializing this class.
     3. `super().__init__(host, user, token)` We are using `super()` to call the `__init__` method of the parent class, BaseApi.
     4. `response = self.session.get(self.endpoint['get_fields'])` We are making a GET request to the `get_fields` endpoint.
     Because we are using session, the authorization header will be implicitly passed. 
     5. `return self.parse_response(response)` This will return the json from the response object
     6. `self.set_path_params(self.endpoint['get_all_issue_field_options'], field_key)` This endpoint uses the path parameters, so we must call the `set_path_params` and pass in the url and path parameters.
     
#### Create issue.py
 1. ##### What is issue.py?
     Just like `fields.py` is responsible for containing the logic for the `fields` endpoints, `issue.py` is responsible for containing the logic for the `issue` endpoints.  
     
 2. ##### What should issue.py look like?
 ```python
from jira_api_wrapper.api.base_api import BaseApi
  
class JiraIssue(BaseApi):
    def __init__(self, host, user, token):
        super().__init__(host, user, token)
    
    def get_issue(self, issue_id_or_key):
        response = self.session.get(
            self.set_path_params(
                self.endpoint['get_issue'],
                issue_id_or_key
            )
        )
        return self.parse_response(response)
 ```
 
 3. ##### What is issue.py doing?
     1. `class JiraIssue(BaseApi)` We are creating a new class for this endpoint, and inheriting from `BaseApi`.
     2. We call `super().__init__(host, user, token)` which will call the `__init__` method of the parent class.
     3. `get_issue` creates a GET request to the `get_issue` endpoint, and uses the `issue_id_or_key` parameter as the path parameter to construct the URL.
     If the response was healthy, we will return the JSON.
     
#### Create api/__init\__.py
 1. ##### What is __init\__.py?
     In the good ol' days of Python2, `__init__.py` was required for to "[make Python treat the directories as containing packages](https://docs.python.org/3/tutorial/modules.html#packages)",
     which basically means that Python would assume there is no code in a directory if `__init__.py` was not present.
     Python3.3 and later does not have this requirement, but it is still commonly used (mostly because our IDEs place it there for us).
     `__init__.py` [Can contain logic](https://docs.python.org/3/tutorial/modules.html#importing-from-a-package) but are usually only used to help manage imports.
     Warning: `__init__.py` will be executed upon importing the package.  
     
 2. ##### What should api/__init\__.py look like?
     ```python
    from jira_api_wrapper.api.fields.fields import JiraFields
    from jira_api_wrapper.api.issue.issue import JiraIssue
     ```
     
 3. ##### What is api/__init\__.py doing?
     The purpose of this is to have a sane way to manage our imports.
     Now in other files when we import these classes, instead of having to have each endpoint class on it's own line, we can simply do:  
     `from jira_api_wrapper.api import JiraFields, JiraIssue`  

#### Create jira_wrapper.py
 1. ##### What is jira_wrapper.py?
     This module will contain a class that inherits from the api classes we have previously created.
 
 2. ##### What should jira_wrapper.py look like?
     ```python
    from jira_api_wrapper.api import JiraIssue, JiraFields

    class JiraWrapper(JiraFields, JiraIssue):
        def __init__(self, host, user, token):
            super().__init__(host, user, token)
     ```
     
 3. ##### What that's it?
     This is just the class that ties all the other classes together into one object.  Now we can do things like 
     ```python
    wrapper = JiraWrapper('http://learn-automation.atlassian.net', 'jonathoncarlyon@gmail.com', 'my-super-secret-token')
    wrapper.get_fields()
    wrapper.get_issue('EI-1')
     ```

#### Create jira_api_wrapper/__init\__.py
 1. ##### What should jira_api_wrapper/__init\__.py look like?
     ```python
    from jira_api_wrapper.wrapper.jira_wrapper import JiraWrapper
     ```
 
 2. ##### Why?
     Once again the answer to why `__init__.py` comes down to imports.
     We know the only thing anybody using this will care about is top level class that inherits from all the other classes, so we can make this easy on the users consuming it.  
     Now when other projects consume this Python package all they need to write is:  
     `from jira_api_wrapper import JiraWrapper`  
     instead of:  
     `from jira_api_wrapper.wrapper.jira_wrapper import JiraWrapper`