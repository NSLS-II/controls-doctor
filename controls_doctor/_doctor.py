import argparse
import subprocess
import os
import re


def gpfs_mount():
    "Checking that GPFS is mounted at /GPFS."
    success = os.path.isdir('/GPFS/')
    return success, ''


def proxy_env():
    "Checking that proxy-related ENV variables are correct."
    http = os.environ.get('http_proxy') == 'http://proxy:8888'
    https = os.environ.get('https_proxy') == 'http://proxy:8888'
    no = os.environ.get('no_proxy') == 'cs.nsls2.local'
    success = http and https and no
    if not success:
        msg = """
    Set environmental variables:

        export http_proxy=http://proxy:8888
        export https_proxy=http://proxy:8888
        export no_proxy=cs.nsls2.local
"""
    else:
        msg = ''
    return success, msg


def condarc():
    "Checking that ~/.condarc does not exist."
    success = not os.path.isfile(os.path.expanduser('~/.condarc'))
    if not success:
        msg = """
Your user-space conda config file may be interfering with system-level
configuration. Delete it like this:

rm ~/.condarc
"""
    else:
        msg = ''
    return success, msg


def binstar_config():
    "Checking that ~/.binstar does not exit."
    success = not os.path.isdir(os.path.expanduser('~/.binstar'))
    if not success:
        msg = """
Your user-space binstar config file may be interfering with system-level
configuration. Delete it like this:

rm -rf ~/binstar
"""
    else:
        msg = ''
    return success, msg


def nfs_perf():
    "Timing NFS performance by writing a 1 MB test file."
    THRESH = 1000000
    o = subprocess.check_output(
            ['dd', 'if=/dev/random', 'of=.check-doctor-dd-testfile',
             'bs=1048576', 'count=1'], stderr=subprocess.STDOUT).decode()
    p = re.compile('.*\((\d+) bytes/sec\)')
    rate = int(p.match(o.split('\n')[-2]).groups(1)[0])
    return rate > THRESH, '{} bytes/sec'.format(rate)


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
    parser.add_argument('--gpfs-mount', action='store_true')
    parser.add_argument('--proxy-env', action='store_true')
    parser.add_argument('--condarc', action='store_true')
    parser.add_argument('--binstar-config', action='store_true')
    parser.add_argument('--nfs-perf', action='store_true')
    parser.add_argument('--conda-env', action='store_true')
    parser.add_argument('--all', action='store_true')
    ns = parser.parse_args()
    print(ns)
    for func in CHECKS:
        if getattr(ns, func.__name__) or ns.all:
            run_check(func)
