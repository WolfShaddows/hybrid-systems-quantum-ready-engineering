@REM Purpose: Maven wrapper launcher. Expected: invoke the project-local Maven distribution with supplied arguments.
@echo off
setlocal
set "ROOT=%~dp0"
set "MAVEN_HOME=%ROOT%tools\apache-maven-3.9.16"
if exist "%MAVEN_HOME%\bin\mvn.cmd" (
  call "%MAVEN_HOME%\bin\mvn.cmd" %*
  exit /b %ERRORLEVEL%
)
where mvn >nul 2>nul
if %ERRORLEVEL% EQU 0 (call mvn %* & exit /b %ERRORLEVEL%)
echo Maven not found. Run scripts\bootstrap-maven.ps1 or install Maven 3.9.16+. 1>&2
exit /b 127



