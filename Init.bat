@echo off
SET rp=%cd%
IF "%PROCESSOR_ARCHITECTURE%"=="x86" (goto 32bit) else (goto 64bit)

:64bit
cd python-3.8.10-embed-amd64
IF EXIST "installd" (
  echo Skipping Install
) ELSE (
  echo.>installd
  call python.exe get-pip.py --isolated --no-deps --no-cache-dir -t .\ blake3-0.1.8-cp38-none-win_amd64.whl setuptools-57.0.0-py3-none-any.whl wheel-0.36.2-py2.py3-none-any.whl pip-21.1.2-py3-none-any.whl psutil-5.8.0-cp38-cp38-win_amd64.whl
)
goto end

:32bit
IF EXIST "installd" (
  echo Skipping Install
) ELSE (
  echo.>installd
  call python.exe get-pip.py --isolated --no-deps --no-cache-dir -t .\ blake3-0.1.8-cp38-none-win32.whl setuptools-57.0.0-py3-none-any.whl wheel-0.36.2-py2.py3-none-any.whl pip-21.1.2-py3-none-any.whl psutil-5.8.0-cp38-cp38-win32.whl
)
cd python-3.8.10-embed-win32
goto end

:end
call python.exe "%rp%\init.py"
cd ..
pause