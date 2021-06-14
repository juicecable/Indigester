@echo off
SET rp=%cd%
IF "%PROCESSOR_ARCHITECTURE%"=="x86" (goto 32bit) else (goto 64bit)

:64bit
cd python-3.8.10-embed-amd64
goto end

:32bit
cd python-3.8.10-embed-win32
goto end

:end
call python.exe "%rp%\delcopy.py"
cd ..
pause