@echo off
setlocal
REM ============================================================
REM  Envia esta pasta para o GitHub:
REM  https://github.com/cbrener89052/calendarioprovas
REM
REM  Basta dar dois cliques neste arquivo.
REM  Quando o Git pedir a senha, use um Personal Access Token.
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
if exist ".git\index.lock" del /f /q ".git\index.lock" >nul 2>&1
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock" >nul 2>&1
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock" >nul 2>&1

if not exist ".git" (
  echo Inicializando o repositorio...
  git init
  if errorlevel 1 goto :erro
  git branch -M main
)

git config user.email "brener53@gmail.com"
git config user.name "Brener"
REM evita o aviso de LF/CRLF nos arquivos de texto
git config core.autocrlf true
git config core.safecrlf false

git remote get-url origin >nul 2>&1
if errorlevel 1 (
  git remote add origin https://github.com/cbrener89052/calendarioprovas.git
) else (
  git remote set-url origin https://github.com/cbrener89052/calendarioprovas.git
)

echo Preparando os arquivos...
git add -A >nul 2>&1
if errorlevel 1 goto :erro

git diff --cached --quiet
if errorlevel 1 (
  echo.
  echo Arquivos alterados:
  git status --short
  echo.
  set "MSG="
  set /p MSG="Mensagem do commit (ENTER usa a padrao): "
  if "%MSG%"=="" set "MSG=Atualiza calendario de provas, scripts e skill"
  git commit -m "%MSG%"
  if errorlevel 1 goto :erro
) else (
  echo Nenhum arquivo novo para preparar.
)

echo.
echo Commits locais:
git log --oneline -5
echo.
echo Enviando para o GitHub...
echo ^(o push acontece mesmo sem arquivos novos, caso haja commit pendente^)
echo.

git push -u origin main
if errorlevel 1 goto :erropush

echo.
echo ================================================
echo   PRONTO! Enviado com sucesso.
echo   https://github.com/cbrener89052/calendarioprovas
echo ================================================
echo.
echo Lembre-se de olhar a branch "main" no GitHub.
goto :fim

:erropush
echo.
echo ================================================
echo   O ENVIO FALHOU
echo ================================================
echo.
echo  1^) Login recusado: a senha da conta nao funciona mais no Git.
echo     Crie um token em https://github.com/settings/tokens
echo     e cole o token no lugar da senha.
echo.
echo  2^) Se aparecer "rejected" ou "non-fast-forward", o repositorio
echo     remoto tem commits que voce nao tem. Rode no terminal:
echo        git pull --rebase origin main
echo     e depois execute este arquivo de novo.
echo.
echo  3^) Para limpar um login errado guardado no Windows:
echo     Painel de Controle ^> Gerenciador de Credenciais ^>
echo     Credenciais do Windows ^> apague a entrada git:https://github.com
echo.
goto :fim

:erro
echo.
echo O comando do Git acima falhou. Veja a mensagem de erro.

:fim
echo.
pause
endlocal
