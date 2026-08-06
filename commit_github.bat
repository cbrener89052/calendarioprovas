@echo off
setlocal
REM ============================================================
REM  Envia esta pasta para o GitHub:
REM  https://github.com/cbrener89052/calendarioprovas
REM
REM  Basta dar dois cliques neste arquivo.
REM  Na primeira vez o Git vai pedir seu login do GitHub:
REM  use um Personal Access Token no lugar da senha.
REM ============================================================
cd /d "%~dp0"
chcp 65001 >nul

echo.
echo ================================================
echo   Calendario de Provas  --^>  GitHub
echo ================================================
echo.

where git >nul 2>&1
if errorlevel 1 (
  echo ERRO: o Git nao esta instalado.
  echo Instale em https://git-scm.com/download/win e rode de novo.
  goto :fim
)

REM --- remove locks de execucoes anteriores que travaram ---
if exist ".git\index.lock" (
  echo Removendo lock antigo do Git...
  del /f /q ".git\index.lock" >nul 2>&1
)
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock" >nul 2>&1
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock" >nul 2>&1
if exist ".git\refs\heads\master.lock" del /f /q ".git\refs\heads\master.lock" >nul 2>&1

if not exist ".git" (
  echo Inicializando o repositorio...
  git init
  if errorlevel 1 goto :erro
  git branch -M main
)

git config user.email "brener53@gmail.com"
git config user.name "Brener"

git remote get-url origin >nul 2>&1
if errorlevel 1 (
  git remote add origin https://github.com/cbrener89052/calendarioprovas.git
) else (
  git remote set-url origin https://github.com/cbrener89052/calendarioprovas.git
)

echo.
echo Preparando os arquivos...
git add -A
if errorlevel 1 goto :erro

echo.
echo Arquivos que serao enviados:
git status --short
echo.

git diff --cached --quiet
if not errorlevel 1 (
  echo Nenhuma mudanca desde o ultimo envio.
  git log --oneline -1 2>nul
  goto :fim
)

set "MSG="
set /p MSG="Mensagem do commit (ENTER usa a padrao): "
if "%MSG%"=="" set "MSG=Atualiza calendario de provas, scripts e skill"

git commit -m "%MSG%"
if errorlevel 1 goto :erro

echo.
echo Enviando para o GitHub...
git push -u origin main
if errorlevel 1 goto :erropush

echo.
echo ================================================
echo   PRONTO! Arquivos enviados com sucesso.
echo   https://github.com/cbrener89052/calendarioprovas
echo ================================================
goto :fim

:erropush
echo.
echo ================================================
echo   O ENVIO FALHOU
echo ================================================
echo Causas comuns:
echo.
echo  1^) Login recusado: a senha da conta nao funciona mais.
echo     Crie um token em https://github.com/settings/tokens
echo     e use o token no lugar da senha.
echo.
echo  2^) O repositorio remoto ja tem commits. Rode no terminal:
echo        git pull --rebase origin main
echo     e depois execute este arquivo de novo.
echo.
goto :fim

:erro
echo.
echo O comando do Git acima falhou. Veja a mensagem de erro.

:fim
echo.
pause
endlocal
