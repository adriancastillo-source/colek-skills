@echo off
rem Instala/actualiza las skills de Colek en la carpeta de skills de Claude Code.
rem Correr con doble clic desde la carpeta del repo descargado.

set "DEST=%USERPROFILE%\.claude\skills"
if not exist "%DEST%" mkdir "%DEST%"

rem borrar la version anterior para que no queden archivos obsoletos instalados
if exist "%DEST%\media-prompting" rmdir /S /Q "%DEST%\media-prompting"
if exist "%DEST%\image-character-sheet" rmdir /S /Q "%DEST%\image-character-sheet"

xcopy /E /I /Y "%~dp0skills\media-prompting" "%DEST%\media-prompting" >nul
xcopy /E /I /Y "%~dp0skills\image-character-sheet" "%DEST%\image-character-sheet" >nul

echo.
echo Listo: skills de Colek instaladas/actualizadas en %DEST%
echo Reinicia tu sesion de Claude Code para que las cargue.
echo.
pause
