import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    author = "Devansh Soni",
    author_email = "sonidev0201@gmail.com",
    name = "Drive-Box",
    version = "1.0.0",
    license = "MIT",
    description = "A GUI application made to download and upload files to Google Drive Storage.",
    url = "https://github.com/devansh-07/Drive-Box",
    # packages = ['Drive'],
    packages=find_packages(),
    package_data={
            'Drive': ['images/*.png', 'secrets/*'],
        },
    long_description=read('README.md'),
    entry_points={'console_scripts': ['mydrive=Drive.main:main']},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
