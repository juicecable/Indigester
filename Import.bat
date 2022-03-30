@echo off
SET rp=%cd%
IF "%PROCESSOR_ARCHITECTURE%"=="x86" (goto 32bit) else (goto 64bit)

:64bit
cd python-3.10.4-embed-amd64
IF EXIST "installd" (
  echo Skipping Install
) ELSE (
  echo.>installd
  call python.exe get-pip.py --isolated --no-deps --no-cache-dir -t .\ blake3-0.3.1-cp310-none-win_amd64.whl setuptools-61.2.0-py3-none-any.whl wheel-0.37.1-py2.py3-none-any.whl pip-22.0.4-py3-none-any.whl psutil-5.9.0-cp310-cp310-win_amd64.whl
)
goto end

:32bit
IF EXIST "installd" (
  echo Skipping Install
) ELSE (
  echo.>installd
  call python.exe get-pip.py --isolated --no-deps --no-cache-dir -t .\ blake3-0.3.1-cp310-none-win32.whl setuptools-61.2.0-py3-none-any.whl wheel-0.37.1-py2.py3-none-any.whl pip-22.0.4-py3-none-any.whl psutil-5.9.0-cp310-cp310-win32.whl
)
cd python-3.10.4-embed-win32
goto end

:end
call python.exe "%rp%\importer.py"
cd ..
pause