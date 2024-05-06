import os
import subprocess


def upload_to_s3(
    relative_path_local: str,
    s3_prefix: str,
    bucket_name: str,
):
    assert os.path.exists(relative_path_local)
    cmd = [
        "mc",
        "cp",
        "-r",
        f"{relative_path_local}/",
        f"{s3_prefix}/{bucket_name}/{relative_path_local}/",
    ]
    subprocess.run(cmd)
