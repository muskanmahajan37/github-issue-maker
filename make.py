from pathlib import Path
from pprint import pprint
from datetime import datetime
import sys
import requests
import json

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = "balloob"
TOKEN = Path(".token").read_text().strip()

# The repository to add this issue to
REPO_OWNER = "home-assistant"
REPO_NAME = "core"


def make_github_issue(title, body=None, assignee=None, milestone=None, labels=None):
    """Create an issue on github.com using the given parameters."""
    # Our url to create issues via POST
    url = "https://api.github.com/repos/%s/%s/issues" % (REPO_OWNER, REPO_NAME)

    # Create our issue
    issue = {
        "title": title,
        "body": body,
        "assignee": assignee,
        "milestone": milestone,
        "labels": labels,
    }

    # Add the issue to our repository
    response = requests.post(
        url, json=issue, headers={"Authorization": "token %s" % TOKEN}
    )

    print(response.status_code)
    pprint(response.json())

    if response.status_code == 201:
        print('Successfully created Issue "%s"' % title)
    else:
        print('Could not create Issue "%s"' % title)
        print("Response:", response.content)


def make_github_issue_no_notify(title, body, labels):
    """Does not fire webhooks or create notifications."""
    # Create an issue on github.com using the given parameters
    # Url to create issues via POST
    url = "https://api.github.com/repos/%s/%s/import/issues" % (REPO_OWNER, REPO_NAME)

    # Headers
    headers = {
        "Authorization": "token %s" % TOKEN,
        "Accept": "application/vnd.github.golden-comet-preview+json",
    }

    # Create our issue
    data = {
        "issue": {
            "title": title,
            "body": body,
            # "created_at": created_at,
            # "closed_at": closed_at,
            # "updated_at": updated_at,
            # "assignee": assignee,
            # "milestone": None,
            # "closed": False,
            "labels": labels,
        }
    }

    # Add the issue to our repository
    response = requests.post(url, json=data, headers=headers)

    print(response.status_code)
    pprint(response.json())

    if response.status_code == 202:
        print('Successfully created Issue "%s"' % title)
    else:
        print('Could not create Issue "%s"' % title)
        print("Response:", response.content)


template = Path("./issues/test_uncaught.markdown").read_text()

for domain in [
    # "abode",
    # "cast",
    # "config",
    "deconz",
    "default_config",
    "demo",
    "discovery",
    "dsmr",
    "dynalite",
    "dyson",
    "gdacs",
    "geonetnz_quakes",
    "homematicip_cloud",
    "hue",
    "ios",
    "local_file",
    "meteo_france",
    "mikrotik",
    "mqtt",
    "plex",
    "qwikswitch",
    "rflink",
    "samsungtv",
    "tplink",
    "tradfri",
    "unifi_direct",
    "upnp",
    "vera",
    "wunderground",
    "yr",
    "zha",
    "zwave",
]:
    title = f"Fix {domain} tests that have uncaught exceptions"
    body = template.replace("{{ DOMAIN }}", domain)
    labels = [f"integration: {domain}", "to do"]
    # print(title)
    # print(body)
    # print(labels)
    make_github_issue(title=title, body=body, labels=labels)
