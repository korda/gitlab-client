from curses_select import select_option
from gitlab_api_client import GitlabApi


def open_project(gitlab_api_client: GitlabApi):
    projects = [project["path_with_namespace"] for project in gitlab_api_client.all_projects()]

    projects.sort()

    select_option(projects)
