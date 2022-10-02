echo off
echo ====================================
echo Initial set-up.
echo ====================================

echo This may take a while...
echo.
echo.
echo.

powershell virtualenv venv
powershell venv/scripts/activate
pip install -r requirements.txt

echo Success. You may now exit.
@pause
exit