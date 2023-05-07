:: Run pytest against gf4
:: This command file must be located in the parent directory of \gf4
@echo off
setlocal
set GF4DIR=%~dp0
set PYTHONPATH=%GF4DIR%\gf4
cd %PYTHONPATH%
py -m pytest -k "not test_smooth and not fit_test"
endlocal
