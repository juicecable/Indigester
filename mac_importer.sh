#!/bin/bash
# check that macOS is used
cd python-mac

python_version="$(python3 --version)"
if [[ "$python_version" == *"Python 3.10"* ]];
then
    echo python 3.10+ already installed
else
    installer -pkg python-3.10.4-macosx11.pkg -target CurrentUserHomeDirectory
# still need to install blake3 and psutil
fi


if [[ "$(pip --version)" == *"pip"* ]]
then
  echo pip already installed
else
  python3 get-pip.py setuptools-61.2.0-py3-none-any.whl wheel-0.37.1-py2.py3-none-any.whl pip-22.0.4-py3-none-any.whl
fi

## install python modules
if [[ "$python_version" == *"Python 3.10"* ]]
then
  pip3 install blake3-0.3.1-cp310-cp310-macosx_11_0_arm64.whl &> /dev/null
  echo "blake3 installed"
  pip3 install psutil-5.9.0-cp310-cp310-macosx_10_9_x86_64.whl &> /dev/null
  echo "psutil installed"
fi

python3 ../importer.py

