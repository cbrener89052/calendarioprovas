@echo off
setlocal
REM ============================================================
REM  Baixa alteracoes do GitHub para esta pasta local.
REM  https://github.com/cbrener89052/calendarioprovas
REM
REM  Use quando outra maquina (ou o Cursor) enviou commits.
REM  Para enviar suas alteracoes, use commit_github.bat.
REM ============================================================
cd /d "%~dp0"
chcp 65001 >nul

echo.
echo ================================================
echo   Atualizar pasta local ^<--  GitHub
echo ================================================
echo.

where git >nul 2>&1
if errorlevel 1 (
  echo ERRO: o Git nao esta instalado.
  goto :fim
)

if not exist ".git" (
  echo ERRO: esta pasta ainda nao esta ligada ao Git.
  echo Execute primeiro: configurar_pasta_local.bat
  goto :fim
)

if exist ".git\index.lock" del /f /q ".git\index.lock" >nul 2>&1

git remote get-url origin >nul 2>&1
if errorlevel 1 (
  git remote add origin https://github.com/cbrener89052/calendarioprovas.git
)

echo Baixando alteracoes da branch main...
git pull --rebase origin main
if errorlevel 1 (
  echo.
  echo A atualizacao falhou. Se houver conflitos, resolva nos arquivos,
  echo depois rode:
  echo   git add -A
  echo   git rebase --continue
  goto :fim
)

echo.
echo ================================================
echo   PRONTO! Pasta atualizada com o GitHub.
echo ================================================

:fim
echo.
pause
endlocal
