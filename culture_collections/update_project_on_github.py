import argparse
import subprocess


def stage_all_and_commit(msg: str = "add new images"):
    subprocess.run(["git", "add", "-A"])
    subprocess.run(["git", "commit", "-m", msg])


def pull(rebase: bool = False) -> bool:
    command = ["git", "pull"]
    if rebase:
        command.append("--rebase")
    pull_process = subprocess.run(command, capture_output=True, text=True)
    if pull_process.stderr:
        print(pull_process.stderr)
    return not pull_process.returncode


def push(remote: str = "origin", branch: str = "main"):
    push_process = subprocess.run(
        ["git", "push", remote, branch], capture_output=True, text=True
    )
    if push_process.stderr:
        print(push_process.stderr)
    return not push_process.returncode


def sync_with_remote():
    is_pulled = pull(rebase=True)
    if not is_pulled:
        return False
    is_pushed = push()
    return is_pushed


def get_args():
    parser = argparse.ArgumentParser(
        description="Sync MoBIE project files with GitHub. No arguments needed."
    )
    parser.parse_args()


def main():
    stage_all_and_commit()
    _ = sync_with_remote()


if __name__ == "__main__":
    get_args()
    # potential merge conflicts need to be solved manually on the command line
    main()
