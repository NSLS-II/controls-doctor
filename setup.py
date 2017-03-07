from distutils.core import setup
import setuptools
import versioneer


setup(name='controls_doctor',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      packages=['controls_doctor'],
      scripts=['scripts/controls-doctor'])
