import subprocess
import os

from combine import Combine


def test_combine_build():
    site_dir = os.path.join(os.path.dirname(__file__), "site")

    # Pretend we are in tests/site
    os.chdir(site_dir)

    combine = Combine(config_path="combine.yml")
    combine.build()

    site_output_dir = os.path.join(site_dir, "output")
    site_output_expected_dir = os.path.join(site_dir, "output_expected")

    res = subprocess.run(["diff", "-w", "-r", site_output_dir, site_output_expected_dir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert res.stdout.decode("utf-8") == ""
    assert res.returncode == 0
