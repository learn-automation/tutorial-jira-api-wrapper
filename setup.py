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
                'jira_api_wrapper.wrapper'],
      )