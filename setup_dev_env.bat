@echo off
echo Checking for administrator privileges...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Administrator privileges confirmed.
) else (
    echo Please run this script as Administrator!
    echo Right-click the batch file and select "Run as administrator"
    pause
    exit /b 1
)

REM Create development directory structure
SET DEV_DIR=D:\Companies\Archive\QGISPlugins\year_range_filter
if not exist "%DEV_DIR%" (
    echo Creating development directory...
    mkdir "%DEV_DIR%"
)

REM Copy plugin files to development directory
echo Copying plugin files to development directory...
xcopy /E /I /Y "%~dp0*.*" "%DEV_DIR%"

REM Create plugin directory if it doesn't exist
SET PLUGIN_DIR=%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\year_range_filter
if exist "%PLUGIN_DIR%" (
    echo Removing existing plugin directory...
    rmdir /S /Q "%PLUGIN_DIR%"
)

echo Creating symbolic link for plugin...
mklink /D "%PLUGIN_DIR%" "%DEV_DIR%"
if %errorLevel% == 0 (
    echo Symbolic link created successfully.
) else (
    echo Failed to create symbolic link!
    pause
    exit /b 1
)

REM Change to development directory
cd /d "%DEV_DIR%"

REM Use system Python for virtual environment
where python >nul 2>&1
if %errorLevel% == 0 (
    echo System Python found successfully.
) else (
    echo System Python not found! Please install Python 3.9 or higher.
    pause
    exit /b 1
)

REM Remove existing venv if it exists
if exist "venv" (
    echo Removing existing virtual environment...
    rmdir /S /Q venv
)

echo Creating Python virtual environment...
python -m venv venv --system-site-packages
if %errorLevel% == 0 (
    echo Virtual environment created successfully.
) else (
    echo Failed to create virtual environment!
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate
if %errorLevel% == 0 (
    echo Virtual environment activated successfully.
) else (
    echo Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Set up QGIS paths after virtual environment activation
SET OSGEO4W_ROOT=D:\OSGeo4W
SET QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis
SET PATH=%OSGEO4W_ROOT%\bin;%PATH%
SET PATH=%OSGEO4W_ROOT%\apps\qgis\bin;%PATH%
SET PATH=%OSGEO4W_ROOT%\apps\qt5\bin;%PATH%
SET PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis\python;%PYTHONPATH%

echo Installing development requirements...
python -m pip install --upgrade pip
pip install pytest pytest-qt pytest-cov black flake8

echo.
echo Development environment setup complete!
echo Plugin development directory: %DEV_DIR%
echo Plugin linked to: %PLUGIN_DIR%
echo.
echo To develop and test the plugin:
echo 1. Open your code editor in: %DEV_DIR%
echo 2. Start QGIS
echo 3. Enable the plugin in Plugins -^> Manage and Install Plugins
echo 4. To run tests:
echo    - Open command prompt in: %DEV_DIR%
echo    - Run: call venv\Scripts\activate
echo    - Run: SET PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis\python;%%PYTHONPATH%%
echo    - Run: pytest test_year_range_filter.py
echo.
echo Note: Make sure to run QGIS as administrator for testing
pause 