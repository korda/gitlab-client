import argparse
from os.path import isdir
from pathlib import Path
from subprocess import check_call

from curses_select import select_option
from gitlab_api_client import GitlabApi
from user_config import get_gitlab_api_client
from user_config import get_project_dir_location


def open_project_action(main_args, progname: str):
    gitlab_instance = main_args.gitlab_instance

    open_project_parser = argparse.ArgumentParser(description='Open project action',
                                                  prog=f'{progname} gitlab_instance open')
    open_project_parser.add_argument('--save-dir-to', dest='saveDirTo',
                                     help='dir path with checked out project will be stored in order to use in '
                                          'bash function to this location')
    open_project_parser.add_argument('--search', dest='search', nargs='?', const='', type=str, default='', required=False,
                                     help='search phrase to narrow projects list')

    args = open_project_parser.parse_args(main_args.args)

    gitlab_api_client = get_gitlab_api_client(gitlab_instance)
    project_dir = get_project_dir_location()

    checkout_dir = __open_project(gitlab_instance, gitlab_api_client, project_dir, args.search)

    if args.saveDirTo:
        Path(args.saveDirTo).write_text(checkout_dir + "\n")


def __open_project(gitlab_instance: str, gitlab_api_client: GitlabApi, project_dir: str, search: str):
    projects = [project["path_with_namespace"] for project in gitlab_api_client.projects(search)]

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
