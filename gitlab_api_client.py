import json
import urllib.parse
import urllib.request
import urllib.error


class GitlabApi:
    def __init__(self, url: str, token: str, checkout_url: str):
        self.__url = url
        self.__token = token
        self.__checkout_url = checkout_url
        self.__api_root = '/api/v4'

    def repo_url(self, path: str) -> str:
        return self.__checkout_url + '/' + path.lstrip('/')

    def get_namespace(self, namespace: str):
        return self.__call('GET', f"namespaces/{urllib.parse.quote(namespace, safe='')}")

    def create_project(self, path: str, namespace_id):
        return self.__call('POST', "projects", path=path, namespace_id=namespace_id, visibility="private")

    def projects(self, search: str):
        if search:
            print("Searching projects containing %s... This make take few moments." % search)
        else:
            print("Getting list of all projects... This make take few moments.")
        projects = []
        per_page = 100
        current_page = 1

        while True:
            current_page_projects = self.__call('GET', "projects",
                                                per_page=per_page,
                                                page=current_page,
                                                simple=True,
                                                archived=False,
                                                search=search
                                                )

            current_page += 1
            projects += current_page_projects

            print(f"{len(projects)} projects retrieved so far...")

            if len(current_page_projects) == 0 or len(current_page_projects) < per_page:
                break

        return projects

    def __call(self, method, api_path, **kwargs):
        query = ''
        if kwargs:
            query = '?' + urllib.parse.urlencode(kwargs)

        request = urllib.request.Request(self.__url + self.__api_root + "/" + api_path.lstrip("/") + query)
        request.add_header('Private-Token', self.__token)
        request.method = method

        return json.loads(urllib.request.urlopen(request).read())
