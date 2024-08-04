@echo off

echo "Checking for staging directory..."
if not exist "C:\dev\website-staging" (
	 mkdir "C:\dev\website-staging"
	 echo "Staging directory not yet created, creating..."
) else (
	echo "Folder already exists..."
)

echo "Done"
pause