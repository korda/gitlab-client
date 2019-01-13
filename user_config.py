import json
from pathlib import Path

from gitlab_api_client import GitlabApi

config_location = Path.home() / ".gitlab-client.json"

def get_gitlab_api_client(gitlab_instance) -> GitlabApi:
    config = __get_gitlab_instance_config(gitlab_instance)
    return GitlabApi(config["url"], config["token"])


def __get_gitlab_instance_config(gitlab_instance):
    #global config_location
    if not config_location.is_file():
        config_location.write_text('{}')

    config = json.loads(config_location.read_text())

    if gitlab_instance not in config:
        provided_url = input("Please provide url to gitlab: ").lstrip().rstrip().rstrip("/")
        provided_token = input("Please provide access token to gitlab: ").lstrip().rstrip()
        config[gitlab_instance] = {
            "url": provided_url,
            "token": provided_token
        }
        config_location.write_text(json.dumps(config, indent=4))
        return __get_gitlab_instance_config(gitlab_instance)

    return config[gitlab_instance]
