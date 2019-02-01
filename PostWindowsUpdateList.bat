@echo off & setlocal enableextensions

::Current Windows Updates list
set outfile="C:\%computername%_WinUpdates\Post_WinUpdates_%computername%_%time:~0,2%%time:~3,2%%time:~6,2%_%date:~-10,2%%date:~-7,2%%date:~-4,4%.csv"

echo Exporting Current Windows updates list to:
echo %outfile%
wmic qfe get > %outfile%
@PAUSE
