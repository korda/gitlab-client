import json
import urllib.request
from pathlib import Path
from curses_select import select_option

config_location = Path.home() / ".gitlab-client.json"
api_root = '/api/v4'


def list_projects(config_name):
    for project in get_gitlab_access(config_name).get("projects"):
        print(project["path_with_namespace"])


def select_project(config_name):
    print("Getting list of all projects... This make take few moments.")
    projects = []
    per_page = 100
    current_page = 1

    while True:
        current_page_projects = [project["path_with_namespace"] for project in get_gitlab_access(config_name)
            .get(f"projects?per_page={per_page}&page={current_page}")]

        current_page += 1
        projects += current_page_projects

        if len(current_page_projects) == 0 or len(current_page_projects) < per_page:
            break

    projects.sort()

    return select_option(projects)


class GitlabAccess:
    def __init__(self, url, token):
        self.__url = url
        self.__token = token

    def get(self, api_path):
        return self._call('GET', api_path)

    def _call(self, method, api_path):
        request = urllib.request.Request(self.__url + api_root + "/" + api_path.lstrip("/"))
        request.add_header('Private-Token', self.__token)
        request.method = method

        return json.loads(urllib.request.urlopen(request).read())


def get_gitlab_access(config_name):
    if not config_location.is_file():
        config_location.write_text('{}')

    config = json.loads(config_location.read_text())

    if config_name not in config:
        provided_url = input("Please provide url to gitlab: ").lstrip().rstrip().rstrip("/")
        provided_token = input("Please provide access token to gitlab: ").lstrip().rstrip()
        config[config_name] = {
            "url": provided_url,
            "token": provided_token
        }
        config_location.write_text(json.dumps(config, indent=4))
        return get_gitlab_access(config_name)

    return GitlabAccess(config[config_name]["url"], config[config_name]["token"])


if __name__ == '__main__':
    print(select_project("unity"))
