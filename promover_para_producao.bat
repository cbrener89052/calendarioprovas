@echo off
setlocal EnableDelayedExpansion
REM ============================================================
REM  Promove o codigo validado da branch main para producao.
REM
REM  Use quando:
REM    - verificar_calendario.py terminou com OK
REM    - voce quer congelar uma versao estavel para a escola
REM
REM  main      = desenvolvimento (Cursor, Reversa, rascunhos)
REM  producao  = versao estavel validada
REM ============================================================
cd /d "%~dp0"
chcp 65001 >nul

echo.
echo ================================================
echo   Promover main --^> producao
echo ================================================
echo.

where git >nul 2>&1
if errorlevel 1 (
  echo ERRO: Git nao instalado.
  goto :fim
)

if not exist ".git" (
  echo ERRO: pasta nao e um repositorio Git.
  goto :fim
)

git diff --quiet
if errorlevel 1 (
  echo ERRO: ha alteracoes nao commitadas.
  echo Commit ou descarte antes de promover.
  git status --short
  goto :fim
)

echo [1/5] Atualizando main do GitHub...
git fetch origin
git checkout main
if errorlevel 1 goto :erro
git pull --rebase origin main
if errorlevel 1 goto :erro

echo.
echo [2/5] Ultimos commits em main:
git log --oneline -5
echo.

set "MSG="
set /p "MSG=Descricao desta promocao (ENTER = Promove versao validada para producao): "
if "!MSG!"=="" set "MSG=Promove versao validada para producao"

echo [3/5] Indo para branch producao...
git checkout producao 2>nul
if errorlevel 1 (
  echo Criando branch producao a partir de main...
  git checkout -b producao
) 

echo [4/5] Mesclando main em producao...
git merge main -m "!MSG!"
if errorlevel 1 (
  echo.
  echo CONFLITO ao mesclar. Resolva manualmente e rode de novo.
  goto :fim
)

echo [5/5] Enviando producao para o GitHub...
git push -u origin producao
if errorlevel 1 goto :erropush

git checkout main

echo.
echo ================================================
echo   PRONTO! Branch producao atualizada.
echo   https://github.com/cbrener89052/calendarioprovas/tree/producao
echo ================================================
echo.
echo Para usar producao no Windows:
echo   git fetch origin
echo   git checkout producao
echo   git pull origin producao
echo.
echo Para voltar ao desenvolvimento:
echo   git checkout main
goto :fim

:erropush
echo Falha no push. Verifique login/token.

:erro
echo Comando Git falhou.

:fim
echo.
pause
endlocal
