@echo off
setlocal EnableDelayedExpansion
REM ============================================================
REM  Roda o scraper de questoes do Super Professor (sprweb).
REM  Primeira vez? Escolha a opcao 1 (modo teste) para validar
REM  antes de rodar uma captura completa.
REM ============================================================
cd /d "%~dp0"
chcp 65001 >nul

echo.
echo ================================================================
echo   Captura de questoes - Super Professor
echo   %CD%
echo ================================================================
echo.

where python >nul 2>&1
if errorlevel 1 (
  echo ERRO: Python nao foi encontrado no PATH.
  echo Instale em https://www.python.org/downloads/ marcando a opcao
  echo "Add python.exe to PATH" durante a instalacao, e rode de novo.
  goto :fim
)

python -c "import playwright" >nul 2>&1
if errorlevel 1 (
  echo [1/2] Instalando dependencias Python ^(playwright^)...
  pip install -r requirements.txt
  if errorlevel 1 goto :erroinstall
  echo [2/2] Baixando o navegador do Playwright ^(so na primeira vez^)...
  python -m playwright install chromium
  if errorlevel 1 goto :erroinstall
) else (
  echo Dependencias ja instaladas.
)

echo.
if "%SPRWEB_EMAIL%"=="" (
  set /p SPRWEB_EMAIL="E-mail do SPR Web / Super Professor: "
)

if "%SPRWEB_SENHA%"=="" (
  for /f "usebackq delims=" %%P in (`powershell -NoProfile -Command "$s = Read-Host 'Senha (nao aparece na tela)' -AsSecureString; $b = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($s); [Runtime.InteropServices.Marshal]::PtrToStringAuto($b)"`) do set "SPRWEB_SENHA=%%P"
)

set /p ENSINO="Ensino [Medio]: "
if "%ENSINO%"=="" set "ENSINO=Medio"

set /p MATERIA="Materia (ex: Matematica, Portugues) [Matematica]: "
if "%MATERIA%"=="" set "MATERIA=Matematica"

echo.
echo Escolha o modo de execucao:
echo   1 = Teste       (mostra o navegador, para em erro, so 5 questoes)
echo   2 = Completo    (roda escondido, captura tudo que encontrar)
echo   3 = Com limite  (voce escolhe quantas questoes capturar)
set /p MODO="Opcao [1]: "
if "%MODO%"=="" set "MODO=1"

if "%MODO%"=="1" (
  python scraper.py --ensino "%ENSINO%" --materia "%MATERIA%" --max-questions 5 --headed --debug
) else if "%MODO%"=="2" (
  python scraper.py --ensino "%ENSINO%" --materia "%MATERIA%"
) else if "%MODO%"=="3" (
  set /p LIMITE="Quantas questoes capturar: "
  python scraper.py --ensino "%ENSINO%" --materia "%MATERIA%" --max-questions !LIMITE!
) else (
  echo Opcao invalida.
  goto :fim
)

goto :fim

:erroinstall
echo.
echo Falha ao instalar dependencias. Veja a mensagem de erro acima.
goto :fim

:fim
echo.
echo Banco de questoes salvo em: questoes.db ^(nesta pasta^)
pause
endlocal
