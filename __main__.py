import argparse
from user_config import get_gitlab_api_client
from user_config import config_location
from open_project import open_project

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gitlab client.')
    parser.add_argument('gitlab_instance', help='you can have multiple gitlab instances to connect to, this argument '
                                                'is required to determine which one to use. if instance is not '
                                                'configured you will be asked to provide configuration with prompt. '
                                                f'configurations are saved in in file {config_location}.')
    parser.add_argument('action', help='action to execute', choices=['open'])
    parser.add_argument('args', nargs=argparse.REMAINDER)

    main_args = parser.parse_args()
    gitlab_instance = main_args.gitlab_instance

    if main_args.action == 'open':
        open_project_parser = argparse.ArgumentParser(description='Open project action',
                                                      prog=f'{parser.prog} gitlab_instance open')
        open_project_parser.parse_args(main_args.args)

        gitlab_api_client = get_gitlab_api_client(gitlab_instance)
        open_project(gitlab_api_client)
    else:
        print(f"Unsupported action {main_args.action}")
        quit(1)

    #print(select_project("unity"))