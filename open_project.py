from pathlib import Path
from subprocess import check_call
from os.path import isdir

from curses_select import select_option
from gitlab_api_client import GitlabApi


def open_project(gitlab_instance: str, gitlab_api_client: GitlabApi, project_dir: str):
    projects = [project["path_with_namespace"] for project in gitlab_api_client.all_projects()]

    projects.sort()

    selected_project = select_option(projects)

    if not selected_project:
        print("No project selected!")
        quit(1)
    else:
        print(f"Selected {selected_project}")

    checkout_dir = str(Path(project_dir) / gitlab_instance / selected_project)

    if not isdir(checkout_dir):
        git_repo_address = gitlab_api_client.repo_url(selected_project)
        print(f"Checking out project from {git_repo_address}")
        check_call(args=['git', 'clone', git_repo_address, checkout_dir])

    return checkout_dir
