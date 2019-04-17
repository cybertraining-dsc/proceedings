"""readme -- a helper to create books from mardown files in a yaml TOC.

Usage:
  readme contrib CLASS DIRECTORY [-v]
  readme projects CLASS DIRECTORY [-v] [--format=FORMAT]
  readme sections CLASS DIRECTORY [-v]
  readme chapters CLASS DIRECTORY [-v]

Arguments:
  YAML   the yaml file

Options:
  -h --help
  -f, --format=FORMAT     [default: github]

Description:

    readme contrib CLASS COMMUNITY

        writes the class list in md format
        COMMUNITY is the directory with all the class repos

"""
import requests
import sys
from pathlib import Path

import oyaml as yaml
# pprint(repos)
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.util import readfile, path_expand
from cloudmesh.variables import Variables
from cloudmesh_installer.install.installer import repos
from docopt import docopt
from tabulate import tabulate

repos_516 = []
repos_222 = []

for repo in repos["spring19"]:
    if "hid-sample" in repo:
        pass
    if "fa18-523-00" in repo:
        pass
    if "-222-" in repo:
        repos_222.append(repo)
    else:
        repos_516.append(repo)

# print (repos_222)
# print (repos_516)


community = "https://github.com/cloudmesh-community"


def class_list(repos, location):
    global community

    owners = []

    for repo in repos:
        try:
            path = f"{location}/{repo}/README.yml"
            path = Path(path).resolve()
            content = readfile(path)
            data = yaml.load(content, Loader=yaml.SafeLoader)
            owner = dotdict(data["owner"])
            owner["url"] = f"{community}/{repo}"
            owners.append(owner)
        except Exception as e:
            print(e)
            VERBOSE(repo)

    return owners


def class_table(repos):
    global community
    headers = ["hid", "firstname", "lastname", "community", "semester", "url"]
    t = []

    for repo in repos:
        try:
            content = readfile(f"./../{repo}/README.yml")
            data = yaml.load(content, Loader=yaml.SafeLoader)
            owner = dotdict(data["owner"])
            url = f"{community}/{repo}"
            t.append(
                [owner.hid, owner.firstname, owner.lastname, owner.community,
                 owner.semester, url])
        except Exception as e:
            print(e)
            VERBOSE(repo)

    print()
    print(tabulate(t, headers=headers))
    print()


def class_artifact(repos, kind):
    global community
    headers = ["hid", "firstname", "lastname", "community", "semester", "url",
               "kind", "title", "Artifact"]
    t = []

    for repo in repos:
        artifact = ""
        title = ""
        try:
            content = readfile(f"./../{repo}/README.yml")
            data = yaml.load(content, Loader=yaml.SafeLoader)
            owner = dotdict(data["owner"])
            url = f"{community}/{repo}"
            t.append(
                [owner.hid, owner.firstname, owner.lastname, owner.community,
                 owner.semester, url, kind, title, artifact])

            # print (data[kind])
            if kind in data:
                artifacts = data[kind]
                for artifact in artifacts:
                    title = "TBD"
                    artifact_url = "TBD"
                    if "title" in artifact:
                        title = artifact["title"]
                    if "url" in artifact:
                        artifact_url = artifact["url"]
                    t.append([owner.hid, owner.firstname, owner.lastname,
                              owner.community, owner.semester, url, kind, title,
                              artifact_url])
            t.append(["", "", "", "", "", "", "", "", ""])
        except Exception as e:
            # print (e)
            # VERBOSE(repo)
            pass

    print()
    print(tabulate(t, headers=headers))
    print()


# class_table(repos_222)

# class_table(repos_516)
"""
VERBOSE("PROJECT")
class_artifact(repos_516, "project")

VERBOSE("CHAPTER")
class_artifact(repos_516, "chapter")
class_artifact(repos_516, "section")
class_artifact(repos_516, "paper")
"""


def create_contributors(owners, location):
    #
    # BUG repo not defined
    #
    global community

    print("# Contributors")
    print()
    t = []
    headers = ["Hid", "Firstname", "Lastname", "Community", "Semester"]

    for owner in owners:
        owner = dotdict(owner)
        hid = owner.hid

        entry = [
            f"[{hid}]({community}/{hid})",
            owner.lastname,
            owner.firstname,
            owner.community,
            owner.semester

        ]
        t.append(entry)
    print(tabulate(t, headers=headers, tablefmt="github"))


def artifact_list(repos, kind, location):
    global community
    artifacts = []

    for repo in repos:
        # print ("Analyzing:", kind, repo)
        path = Path(f"{location}/{repo}/README.yml").resolve()
        try:
            content = readfile(path)
            data = yaml.load(content, Loader=yaml.SafeLoader)
            if kind in data:
                for entry in data[kind]:
                    # print (type(entry), type(data["owner"]))
                    # print (entry, data["owner"])
                    entry.update(data["owner"])
                    # print (entry)
                    artifacts.append(entry)
        except Exception as e:
            print(e)
            VERBOSE(repo)
            pass
    return artifacts


def main():
    arguments = dotdict(docopt(__doc__))
    verbose = arguments["-v"]
    v = Variables()
    if verbose:
        v["verbose"] = "10"
    else:
        v["verbose"] = "0"

    # arguments["FORMAT"] = arguments["--format"]
    location = path_expand(arguments.DIRECTORY)

    VERBOSE(arguments)

    if arguments.CLASS in ["5", "516", "e516"]:
        repos = repos_516
    elif arguments.CLASS in ["2", "222", "e222"]:
        repos = repos_222
    else:
        print("your class is not yet supported")
        sys.exit(10)

    if arguments.contrib:

        owners = class_list(repos, location)
        create_contributors(owners, location)

    elif arguments.projects:

        print("# Project List")
        print()
        artifacts = artifact_list(repos, "project", location)

        t = []
        for entry in artifacts:

            if "url" in entry:
                entry["link"] = entry["url"]
                if ".md" not in entry["url"]:
                    entry["link"] = entry["url"] = None
            else:
                entry["link"] = entry["url"] = None

            title = entry["title"]

            url = entry["url"]

            if url is not None:
                try:

                    r = requests.get(url, allow_redirects=True)
                    if r.status_code == 200:
                        url = f"[url]({url})"
                    else:
                        url = ":o: invalid "

                except:
                    url = ":o: invalid "

            else:
                url = ":o: ERROR: not an md file"

            if "TBD" == title:
                title = ":o: ERROR: no title specified"
            link = entry["link"]
            if entry["lastname"] != "TBD":
                t.append([
                    "[{hid}](https://github.com/cloudmesh-community/{hid})".format(**entry),
                    entry["lastname"],
                    entry["firstname"],
                    url,
                    title
                ])

        print(tabulate(t,
                       headers=["Hid", "Lastname", "Firstname", "Url", "Title"],
                       tablefmt=arguments["--format"]))


if __name__ == '__main__':
    main()
