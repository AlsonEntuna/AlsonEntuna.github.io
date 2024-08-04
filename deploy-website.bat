@echo off

echo Deploying website...

set web_staging_location="C:\dev\website-staging"
echo Staging location: %web_staging_location%

set web_deployment_location="%DEV_WEBSITE_DIR%"
echo Deployment location: %web_deployment_location%

xcopy /exclude:exclusionlist.txt /s /y "%web_staging_location%" "%web_deployment_location%"

pause