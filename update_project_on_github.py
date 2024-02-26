import subprocess


def stage_all_and_commit(msg="add new images"):
    subprocess.run(["git", "add", "-A"])
    subprocess.run(["git", "commit", "-m", msg])


def pull(rebase: bool = False) -> bool:
    command = ["git", "pull"]
    if rebase:
        command.append("--rebase")
    pull_process = subprocess.run(command, capture_output=True, text=True)
    if pull_process.stderr:
        print(pull_process.stderr)
    return not pull_process.stderr


def push(remote: str = "origin", branch: str = "main"):
    push_process = subprocess.run(
        ["git", "push", remote, branch], capture_output=True, text=True
    )
    if push_process.stderr:
        print(push_process.stderr)
    is_pushed = not push_process.stderr
    # git writes output to stderr, so we need to check for the desired output
    if push_process.stderr.startswith(
        "To github.com:Dey-Lab-Team/culture-collections.git"
    ):
        is_pushed = True
    return is_pushed


def sync_with_remote():
    is_pulled = pull(rebase=True)
    if not is_pulled:
        return False
    is_pushed = push()
    return is_pushed


# make changes to test


def main():
    stage_all_and_commit()
    _ = sync_with_remote()


if __name__ == "__main__":
    # potential merge conflicts need to be solved manually on the command line
    main()
