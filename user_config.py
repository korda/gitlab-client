import json
from os.path import isdir
from os import mkdir
from pathlib import Path

from gitlab_api_client import GitlabApi

config_location = Path.home() / ".gitlab-client.json"


def get_gitlab_api_client(gitlab_instance) -> GitlabApi:
    config = __get_gitlab_instance_config(gitlab_instance)
    return GitlabApi(config["url"], config["token"], config["checkout_url"])


def get_project_dir_location() -> str:
    config = __load_config()
    project_dir_key = 'project_dir'

    if project_dir_key not in config:
        provided_dir = input("Please provide directory for project checkout: ").lstrip().rstrip().rstrip("/")
        if not provided_dir.startswith("/"):
            provided_dir = Path.home() / provided_dir

        print(f"Saving {provided_dir} as project checkout directory...")
        config[project_dir_key] = str(provided_dir.absolute())
        __save_config(config)

    if not isdir(config[project_dir_key]):
        mkdir(config[project_dir_key])

    return config[project_dir_key]


def __get_gitlab_instance_config(gitlab_instance):
    config = __load_config()
    gitlab_instances_key = 'gitlab_instances'

    if config[gitlab_instances_key] is None:
        config[gitlab_instances_key] = {}

    if gitlab_instance not in config[gitlab_instances_key]:
        provided_url = input("Please provide url to gitlab: ").lstrip().rstrip().rstrip("/")
        provided_token = input("Please provide access token to gitlab: ").lstrip().rstrip()
        config[gitlab_instances_key][gitlab_instance] = {
            "url": provided_url,
            "token": provided_token
        }
        __save_config(config)

    if "checkout_url" not in config[gitlab_instances_key][gitlab_instance]:
        default_url = config[gitlab_instances_key][gitlab_instance]["url"]
        default_url = default_url.replace("https://", "").replace("http://", "")
        default_url = f"ssh://git@{default_url}"

        checkout_url = input(f"Please provide url base for checkout [{default_url}]: ").lstrip().rstrip().rstrip("/")
        if not checkout_url:
            checkout_url = default_url

        config[gitlab_instances_key][gitlab_instance]["checkout_url"] = checkout_url
        __save_config(config)

    return config[gitlab_instances_key][gitlab_instance]


def __save_config(config):
    config_location.write_text(json.dumps(config, indent=4))


def __load_config():
    __ensure_config_file_exists()
    return json.loads(config_location.read_text())


def __ensure_config_file_exists():
    if not config_location.is_file():
        config_location.write_text('{}')
