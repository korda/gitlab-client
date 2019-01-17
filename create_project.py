import argparse

from gitlab_api_client import GitlabApi
from user_config import get_gitlab_api_client
from subprocess import check_call


def create_project_action(main_args, progname: str):
    gitlab_instance = main_args.gitlab_instance

    create_project_parser = argparse.ArgumentParser(description='Create new project',
                                                  prog=f'{progname} gitlab_instance create')
    create_project_parser.add_argument('path',
                                       help='path of project to create')

    args = create_project_parser.parse_args(main_args.args)

    gitlab_api_client = get_gitlab_api_client(gitlab_instance)

    __create_project(gitlab_api_client, args.path)


def __create_project(gitlab_api_client: GitlabApi, path: str):
    #gitlab_api_client.create_project(path)
    groups = path.split("/")
    path = groups.pop()

    prev_group = None
    group = None
    for group_path in groups:

        for found in gitlab_api_client.find_namespace(group_path):
            if found['path'] == group_path and ((prev_group is None and found['parent_id'] is None)
                                                or prev_group['id'] == found['parent_id']):
                group = found
                break

        prev_group = group

    repo = gitlab_api_client.create_project(path, group['id'])

    print(f"Created repo with url {repo['ssh_url_to_repo']}")
    print(f"Gitlab link: {repo['web_url']}")

    check_call(args=['git', 'remote', 'add', 'origin', repo['ssh_url_to_repo']])

    # git remote add github git@github.com:Unity-Group/hipchat-download-emoji.git
