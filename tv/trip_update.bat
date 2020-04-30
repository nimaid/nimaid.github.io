@echo off

set ORIGDIR="%CD%"
set SCRIPTDIR="%~dp0"

cd %SCRIPTDIR%

echo Running updater script...

call conda activate tv.nimaid.com
call python trip_update.py
if errorlevel 1 goto ERROR

goto DONE

:ERROR
call conda deactivate
cd %ORIGDIR%
echo Updater script failed!
pause
exit /B 1

:DONE
call conda deactivate
cd %ORIGDIR%
echo Updater script done!
pause
exit /B 0