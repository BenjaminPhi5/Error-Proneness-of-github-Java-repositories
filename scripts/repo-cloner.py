import git

"""
Given a repository url and a path to a directory
clone the repository in the directory
"""


def clone_repository(dir_path, repo_url):
    # adds the .git on the end for the actual cloning url
    git.Git(dir_path).clone(repo_url + ".git")


#clone_repository("clone-testing-folder/", "https://github.com/BenjaminPhi5/Mix-Tab")

