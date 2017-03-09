# controls-doctor

A command-line utility that checks for common problems related to IT or DAMA.

To get help. use ``controls-doctor --help`` or ``controls-doctor -h``.

Example:

```
$ controls-doctor --all
✗ Checking that GPFS is mounted at /GPFS.

    The GPFS could be found at /GPFS. If you have any detectors that write to
    the GPFS, you will not be able to access their data from here. Contact the
    IT group if you need access.

✗ Checking that proxy-related ENV variables are correct.

    Set environmental variables:

        export http_proxy=http://proxy:8888
        export https_proxy=http://proxy:8888
        export no_proxy=cs.nsls2.local

✗ Checking that ~/.condarc does not exist.

    Your user-space conda config file may be interfering with system-level
    configuration. Delete it like this:

        rm ~/.condarc

✓ Checking that ~/.binstar does not exit.
✗ Timing NFS performance by writing a 1 MB test file.

    The filesystem seems to be slow. A quick test writing 1 MB ran at
    9738788 bytes/sec. As a result, programs may be unresponsive. Contact the IT
    group.

✗ Checking conda env from standard user or system location is activated.
    Current Python is at /Users/dallan/miniconda/envs/bnl/bin/python
```

## Installation

```
git clone https://github.com/NSLS-II/controls-doctor
cd controls-doctor
pip install .
```
