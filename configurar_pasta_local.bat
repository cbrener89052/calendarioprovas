@echo off
setlocal EnableDelayedExpansion
REM ============================================================
REM  Liga esta pasta (com arquivos ja existentes) ao GitHub:
REM  https://github.com/cbrener89052/calendarioprovas
REM
REM  Use na primeira vez, quando a pasta ainda nao tem .git
REM  ou quando o remoto ainda nao esta configurado.
REM  Depois disso, use commit_github.bat (enviar) e
REM  atualizar_do_github.bat (baixar).
REM ============================================================
cd /d "%~dp0"
chcp 65001 >nul

echo.
echo ================================================================
echo   Configurar pasta local ^<--^> GitHub
echo   %CD%
echo ================================================================
echo.

where git >nul 2>&1
if errorlevel 1 (
  echo ERRO: o Git nao esta instalado.
  echo Instale em https://git-scm.com/download/win e rode de novo.
  goto :fim
)

REM --- remove locks de execucoes anteriores que travaram ---
if exist ".git\index.lock" del /f /q ".git\index.lock" >nul 2>&1
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock" >nul 2>&1

git config user.email "brener53@gmail.com"
git config user.name "Brener"
git config core.autocrlf true
git config core.safecrlf false

if not exist ".git" (
  echo [1/5] Inicializando repositorio Git nesta pasta...
  git init
  if errorlevel 1 goto :erro
  git branch -M main
) else (
  echo [1/5] Repositorio Git ja existe nesta pasta.
)

git remote get-url origin >nul 2>&1
if errorlevel 1 (
  echo [2/5] Adicionando remoto origin...
  git remote add origin https://github.com/cbrener89052/calendarioprovas.git
) else (
  echo [2/5] Ajustando URL do remoto origin...
  git remote set-url origin https://github.com/cbrener89052/calendarioprovas.git
)

echo [3/5] Baixando historico do GitHub...
git fetch origin
if errorlevel 1 goto :errofetch

git rev-parse --verify HEAD >nul 2>&1
if errorlevel 1 (
  echo [4/5] Primeiro commit com os arquivos desta pasta...
  git add -A
  git commit -m "Estado local inicial da pasta calendarioprovas"
  if errorlevel 1 goto :erro
)

echo [4/5] Unindo com a branch main do GitHub...
git branch -M main
git pull origin main --allow-unrelated-histories --no-edit
if errorlevel 1 (
  echo.
  echo ATENCAO: houve conflito ao unir com o GitHub.
  echo Abra o terminal nesta pasta, resolva os conflitos e rode:
  echo   git add -A
  echo   git commit -m "Resolve conflitos iniciais com o GitHub"
  echo   git push -u origin main
  goto :fim
)

echo [5/5] Enviando e configurando acompanhamento da branch main...
git push -u origin main
if errorlevel 1 goto :erropush

echo.
echo ================================================================
echo   PRONTO! Pasta sincronizada com o GitHub.
echo   https://github.com/cbrener89052/calendarioprovas
echo.
echo   Enviar alteracoes locais:  commit_github.bat
echo   Baixar alteracoes remotas: atualizar_do_github.bat
echo ================================================================
goto :fim

:errofetch
echo.
echo Nao foi possivel baixar do GitHub. Verifique internet e login.
echo Se pedir senha, use um Personal Access Token:
echo   https://github.com/settings/tokens
goto :fim

:erropush
echo.
echo O envio falhou. Se o GitHub tiver commits que voce nao tem, rode:
echo   atualizar_do_github.bat
echo e depois execute este arquivo de novo.
goto :fim

:erro
echo.
echo O comando do Git acima falhou. Veja a mensagem de erro.

:fim
echo.
pause
endlocal
