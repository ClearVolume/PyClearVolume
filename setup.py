import os
from setuptools import setup


setup(name='pyclearvolume',
      version='0.1',
      description='python binding for the ClearVolume Renderer',
      url='http://bitbucket.org/clearvolume/pyclearvolume',
      author='Martin Weigert',
      author_email='mweigert@mpi-cbg.de',
      license='MIT',
      packages=['pyclearvolume'],
      install_requires=["numpy","scipy","sortedcontainers"],
      entry_points={
          'console_scripts': [
              'pycleartest=pyclearvolume.test:main',
              'pyclearvolume_serve=pyclearvolume.pyclearvolume_serve:main',
          ],
      }

      
      # package_data={"":['']},
)
