import argparse

from open_project import open_project_action
from create_project import create_project_action
from user_config import config_location

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gitlab client.')
    parser.add_argument('gitlab_instance', help='you can have multiple gitlab instances to connect to, this argument '
                                                'is required to determine which one to use. if instance is not '
                                                'configured you will be asked to provide configuration with prompt. '
                                                f'configurations are saved in in file {config_location}.')
    parser.add_argument('action', help='action to execute', choices=['open', 'create'])
    parser.add_argument('args', nargs=argparse.REMAINDER)

    main_args = parser.parse_args()

    if main_args.action == 'open':
        open_project_action(main_args, parser.prog)
    elif main_args.action == 'create':
        create_project_action(main_args, parser.prog)
    else:
        print(f"Unsupported action {main_args.action}")
        quit(1)
