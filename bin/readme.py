from  cloudmesh_installer.install.installer import repos
from pprint import pprint
import oyaml as yaml
from cloudmesh.common.util import readfile
#pprint(repos)
from cloudmesh.DEBUG import VERBOSE
from tabulate import tabulate
from cloudmesh.common.dotdict import dotdict

repos_516 = []
repos_222 = []

for repo in repos["spring19"]:
    if "-222-" in repo:
        repos_222.append(repo)
    else:
        repos_516.append(repo)

print (repos_222)
print (repos_516)


community="https://github.com/cloudmesh-community"

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
            t.append([owner.hid, owner.firstname, owner.lastname, owner.community, owner.semester, url])
        except Exception as e:
            print (e)
            VERBOSE(repo)

    print()
    print(tabulate(t, headers=headers))
    print()




def class_artifact(repos, kind):
    global community
    headers = ["hid", "firstname", "lastname", "community", "semester", "url", "kind", "title", "Artifact"]
    t = []

    for repo in repos:
        artifact = ""
        title = ""
        try:
            content = readfile(f"./../{repo}/README.yml")
            data = yaml.load(content, Loader=yaml.SafeLoader)
            owner = dotdict(data["owner"])
            url = f"{community}/{repo}"
            t.append([owner.hid, owner.firstname, owner.lastname, owner.community, owner.semester, url, kind, title, artifact])


            print (data[kind])
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

        except Exception as e:
            print (e)
            VERBOSE(repo)

    print()
    print(tabulate(t, headers=headers))
    print()

#class_table(repos_222)

#class_table(repos_516)

class_artifact(repos_516, "project")
