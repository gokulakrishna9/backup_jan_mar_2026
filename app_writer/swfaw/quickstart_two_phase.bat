@echo off
REM Quick start script for two-phase workflow (Windows)

echo ==================================
echo swfaw_v2 Two-Phase Quick Start
echo ==================================
echo.

if "%1"=="" (
    echo Usage: quickstart_two_phase.bat ^<sql_or_json_file^> [output_directory]
    echo.
    echo Examples:
    echo   quickstart_two_phase.bat ..\mysql_database_design\schema.sql
    echo   quickstart_two_phase.bat ..\mysql_database_design\schema.sql ..\generated_application\my_app
    exit /b 1
)

set INPUT_FILE=%1
set OUTPUT_DIR=%2

if "%OUTPUT_DIR%"=="" (
    for %%I in (%INPUT_FILE%) do set BASENAME=%%~nI
    set OUTPUT_DIR=..\generated_application\%BASENAME%_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
    set OUTPUT_DIR=%OUTPUT_DIR: =0%
)

echo Input: %INPUT_FILE%
echo Output: %OUTPUT_DIR%
echo.

REM Run unified workflow
python generate_app.py --input "%INPUT_FILE%" --output "%OUTPUT_DIR%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==================================
    echo Generation Complete!
    echo ==================================
    echo.
    echo Next steps:
    echo 1. Setup database:
    echo    mysql -u root -p -e "CREATE DATABASE your_db_name;"
    echo    mysql -u root -p your_db_name ^< %OUTPUT_DIR%\auth-schema.sql
    echo    mysql -u root -p your_db_name ^< %OUTPUT_DIR%\activity-tracking-schema.sql
    echo.
    echo 2. Build and run:
    echo    cd %OUTPUT_DIR%
    echo    mvn clean install
    echo    mvn spring-boot:run
    echo.
    echo 3. Complete setup at: http://localhost:8081/setup
) else (
    echo.
    echo Generation failed. Check errors above.
    exit /b 1
)
