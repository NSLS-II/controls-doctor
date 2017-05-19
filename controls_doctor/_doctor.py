import argparse
import subprocess
import os
import re


def gpfs_mount():
    "Checking that GPFS is mounted at /GPFS."
    success = os.path.isdir('/GPFS/')
    msg = """
    The GPFS could be found at /GPFS. If you have any detectors that write to
    the GPFS, you will not be able to access their data from here. Contact the
    IT group if you need access.
"""
    return success, msg


def proxy_env():
    "Checking that proxy-related ENV variables are correct."
    http = os.environ.get('http_proxy') == 'http://proxy:8888'
    https = os.environ.get('https_proxy') == 'http://proxy:8888'
    no = os.environ.get('no_proxy') == 'cs.nsls2.local'
    success = http and https and no
    msg = """
    Set environmental variables:

        export http_proxy=http://proxy:8888
        export https_proxy=http://proxy:8888
        export no_proxy=cs.nsls2.local
"""
    return success, msg


def condarc():
    "Checking that ~/.condarc does not exist."
    success = not os.path.isfile(os.path.expanduser('~/.condarc'))
    msg = """
    Your user-space conda config file may be interfering with system-level
    configuration. Delete it like this:

        rm ~/.condarc
"""
    return success, msg


def binstar_config():
    "Checking that ~/.binstar does not exit."
    success = not os.path.isdir(os.path.expanduser('~/.binstar'))
    msg = """
    Your user-space binstar config file may be interfering with system-level
    configuration. Delete it like this:

        rm -rf ~/binstar

    (Be especially careful using the `rm -rf` command. Typing the wrong thing
    can be destructive!)
"""
    return success, msg


def nfs_perf():
    "Timing NFS performance by writing a 1 MB test file."
    THRESH = 1000000
    output_path = os.path.expanduser('~/.check-doctor-dd-testfile')
    output = subprocess.check_output(
            ['dd', 'if=/dev/random', 'of={}'.format(output_path),
             'bs=1048576', 'count=1'], stderr=subprocess.STDOUT).decode()
    for line in output.split('\n'):
        if line.endswith('/s') or line.endswith('/sec'):
            rate = float(line.split()[-2])
            break
    msg = """
    The filesystem seems to be slow. A quick test writing 1 MB ran at
    {} bytes/sec. As a result, programs may be unresponsive. Contact the IT
    group.
""".format(rate)
    return rate > THRESH, msg


def conda_env():
    "Checking conda env from standard user or system location is activated."
    o = subprocess.check_output(['which', 'python']).decode()
    is_system_conda_env = o.startswith('/opt/conda_env')
    is_user_conda_env = o.startswith(os.path.expanduser('~/conda_envs'))
    success = is_system_conda_env or is_user_conda_env
    msg = '    Current Python is at {}'.format(o)
    return success, msg

CHECKS = [
    gpfs_mount,
    proxy_env,
    condarc,
    binstar_config,
    nfs_perf,
    conda_env,
]

def run_check(func):
    print("  {}".format(func.__doc__))
    success, msg = func()
    if success:
        print('\033[92m\x1b[1A\u2713\033[0m')
    else:
        print('\033[91m\x1b[1A\u2717\033[0m')
        print(msg)

def main():
    parser = argparse.ArgumentParser()
    for func in CHECKS:
        name_as_flag = '--{}'.format(func.__name__.replace('_', '-').lower())
        parser.add_argument(name_as_flag, action='store_true',
                            help=func.__doc__)
    parser.add_argument('--all', action='store_true', help='All of the above.')
    ns = parser.parse_args()
    for func in CHECKS:
        if getattr(ns, func.__name__) or ns.all:
            run_check(func)
