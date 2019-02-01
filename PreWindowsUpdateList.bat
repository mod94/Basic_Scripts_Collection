@echo off & setlocal enableextensions
:: folder details
set outdir="c:\%computername%_WinUpdates"

::Current Windows Updates list
set outdirile="%outdir%\PRE_WinUpdates_%computername%_%time:~0,2%%time:~3,2%%time:~6,2%_%date:~-10,2%%date:~-7,2%%date:~-4,4%.csv"

:: check for existence of WinUpdates
:: if WinUpdates doesn't exist, create it
if not exist "%outdir%\" (
  echo folder "%outdir%" not found
  echo creating folder "%outdir%"
  md "%outdir%"
  goto ExportList
  )

:ExportList
echo Exporting Current Windows updates list to:
echo %outdirile%
wmic qfe get > %outdirile%
@PAUSE
