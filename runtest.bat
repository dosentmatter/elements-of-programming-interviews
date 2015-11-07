@echo off
set argC=0
for %%x in (%*) do set /A argC+=1

if %argC% EQU 0 (
    python -m unittest discover -v
) else if  "%~1"=="unit" (
    python -m unittest discover -v -p test_unit*.py
) else if "%~1"=="performance" (
    python -m unittest discover -v -p test_performance*.py
) else (
    @echo on
    echo Incorrect parameter "%~1". Usage: runtest.bat ^[unit^|performance^]
    @echo off
)

REM This checks cmdcmdline for "/c". If it exists, that means this .bat was
REM double clicked. The "%%~x" adds quotes on the outside "" and the tilde means
REM to remove quotes leaving only one pair of quotes and not two.
REM This only pauses if double clicked.
for %%x in (%cmdcmdline%) do if /i "%%~x"=="/c" set DOUBLECLICKED=1
if defined DOUBLECLICKED pause