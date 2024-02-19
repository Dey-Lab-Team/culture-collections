import subprocess


def stage_all_and_commit(msg="add new images"):
    subprocess.run(["git", "add", "-A"])
    subprocess.run(["git", "commit", "-m", msg])


def pull(rebase: bool = False) -> bool:
    command = ["git", "pull"]
    if rebase:
        command.append("--rebase")
    pull_process = subprocess.run(
        command,
        capture_output=True,
        text=True
    )
    if pull_process.stderr:
        print(pull_process.stderr)
    return not pull_process.stderr


def push():
    push_process = subprocess.run(
        ["git", "push"],
        capture_output=True,
        text=True
    )
    if push_process.stderr:
        print(push_process.stderr)
    return not push_process.stderr


def sync_with_remote():
    is_pulled = pull(rebase=True)
    if not is_pulled:
        return False
    is_pushed = push()
    return is_pushed


def main():
    stage_all_and_commit()
    _ = sync_with_remote()


if __name__ == "__main__":
    # potential merge conflicts need to be solved manually on the command line
    main()
