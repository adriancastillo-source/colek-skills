@echo off
rem Instala/actualiza las skills de Colek en la carpeta de skills de Claude Code.
rem Correr con doble clic desde la carpeta del repo descargado.

set "DEST=%USERPROFILE%\.claude\skills"
if not exist "%DEST%" mkdir "%DEST%"

xcopy /E /I /Y "%~dp0skills\media-prompting" "%DEST%\media-prompting" >nul
xcopy /E /I /Y "%~dp0skills\image-character-sheet" "%DEST%\image-character-sheet" >nul

echo.
echo Listo: skills de Colek instaladas/actualizadas en %DEST%
echo Reinicia tu sesion de Claude Code para que las cargue.
echo.
pause
