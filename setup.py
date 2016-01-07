from setuptools import setup

setup(name='imgur_downloader',
      version='0.1.0',
      packages=['imgur_downloader'],
      entry_points={
          'console_scripts': [
              'imgur_downloader = imgur_downloader.__main__:main'
          ]
      },
      )
