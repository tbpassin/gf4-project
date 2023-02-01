:: Run pytest against gf4
@echo off
setlocal
set PYTHONPATH=c:\tom\git\gf4-project\gf4
py -m pytest -k "not test_smooth and not fit_test"
endlocal
