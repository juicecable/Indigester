#!/bin/bash
# check that macOS is used
cd python-mac

python_version="$(python3 --version)"
if [[ "$python_version" == *"Python 3.8"* ]] || [[ "$python_version" == *"Python 3.9"* ]];
then
    echo python 3.8+ already installed
else
    installer -pkg python-3.8.10-macosx10.9.pkg -target CurrentUserHomeDirectory
# still need to install blake3 and psutil
fi


if [[ "$(pip --version)" == *"pip"* ]]
then
  echo pip already installed
else
  python3 get-pip.py setuptools-57.0.0-py3-none-any.whl wheel-0.36.2-py2.py3-none-any.whl pip-21.1.2-py3-none-any.whl
fi

## install python modules
if [[ "$python_version" == *"Python 3.8"* ]]
then
  pip3 install blake3-0.1.8-cp38-cp38-macosx_10_7_x86_64.whl &> /dev/null
  echo "blake3 installed"
  pip3 install psutil-5.8.0-cp38-cp38-macosx_10_9_x86_64.whl &> /dev/null
  echo "psutil installed"
else
  pip3 install blake3-0.1.8-cp39-cp39-macosx_10_7_x86_64.whl &> /dev/null
  echo "blake3 installed"
  pip3 install psutil-5.8.0-cp39-cp39-macosx_10_9_x86_64.whl &> /dev/null
  echo 'psutil installed'
fi

python3 ../importer.py


