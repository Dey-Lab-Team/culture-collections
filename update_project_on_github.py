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
    # potential merge conflicts need to be solved manually on the command line
    main()
