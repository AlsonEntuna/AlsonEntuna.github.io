@echo off

set web_location="C:\dev\website-staging"
set current_directory=%cd%
echo "Current directory: %current_directory%"

echo "Checking for staging directory..."
if not exist %web_location% (
	 mkdir %web_location%
	 echo "Staging directory not yet created, creating..."
) else (
	echo "Folder already exists..."
)

echo "Setting environment variable..."

setx DEV_WEBSITE_DIR %current_directory%
echo "Env variable DEV_WEBSITE_DIR set to: %current_directory%"

pause