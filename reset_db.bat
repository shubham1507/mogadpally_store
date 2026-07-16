@echo off
setlocal EnableDelayedExpansion

echo ==========================================
echo MOGADPALLY STORE - FULL RESET
echo ==========================================

REM PostgreSQL
set PGPASSWORD=snj
set PG_BIN=C:\Program Files\PostgreSQL\17\bin

set DB_NAME=mogadpally_store
set DB_USER=postgres
set DB_HOST=localhost
set DB_PORT=5432

echo.
echo ==========================================
echo Deleting migration files...
echo ==========================================

for %%D in (
users
catalog
cart
orders
payments
) do (

    if exist apps\%%D\migrations (

        del /Q apps\%%D\migrations\0*.py >nul 2>&1

        if exist apps\%%D\migrations\__pycache__ (
            rmdir /S /Q apps\%%D\migrations\__pycache__
        )

        echo Cleaned %%D migrations
    )
)

echo.
echo ==========================================
echo Dropping database...
echo ==========================================

"%PG_BIN%\dropdb.exe" ^
-h %DB_HOST% ^
-p %DB_PORT% ^
-U %DB_USER% ^
--if-exists ^
%DB_NAME%

echo.
echo ==========================================
echo Creating database...
echo ==========================================

"%PG_BIN%\createdb.exe" ^
-h %DB_HOST% ^
-p %DB_PORT% ^
-U %DB_USER% ^
%DB_NAME%

echo.
echo ==========================================
echo Creating migrations...
echo ==========================================

python manage.py makemigrations

if errorlevel 1 goto ERROR

echo.
echo ==========================================
echo Running migrations...
echo ==========================================

python manage.py migrate

if errorlevel 1 goto ERROR

echo.
echo ==========================================
echo Seeding Products...
echo ==========================================

python manage.py seed_products

echo.
echo ==========================================
echo Creating Superuser (optional)
echo ==========================================

echo Run manually if needed:
echo python manage.py createsuperuser

echo.
echo ==========================================
echo RESET COMPLETED SUCCESSFULLY
echo ==========================================

pause
exit /b

:ERROR
echo.
echo ==========================================
echo RESET FAILED!
echo ==========================================
pause
exit /b 1