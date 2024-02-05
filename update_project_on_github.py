import subprocess


def stage_all_and_commit(msg="add new images"):
    subprocess.run(["git", "add", "-A"])
    subprocess.run(["git", "commit", "-m", msg])


def sync_with_remote():
    subprocess.run(["git", "pull"])
    subprocess.run(["git", "push"])


def main():
    stage_all_and_commit()
    sync_with_remote()


if __name__ == "__main__":
    # potential merge conflicts need to be saved manually on the command line
    main()


# git pull before I change anything (do this in code)
# git stage
# git commit
# git pull
# solve potential merge conflicts
# git push

# either people need a gihub account and I add them as a collaborator
# or everyone gets the password to the deylab github account

# I should git pull before I add files
# check if git repo is here (must be)
# find new/modified files and satge them
    # check for gitignore
# commit
    # use certain commit message
# push
    # is already pulled?
