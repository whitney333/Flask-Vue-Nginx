@echo off
SET /P AWSCLI="Check if AWS CLI is installed. Press Enter to continue..."
aws --version
if %ERRORLEVEL% neq 0 (
    echo AWS CLI is not installed.
    SET /P INSTALL="Do you want to install AWS CLI now? [Y/N]: "
    if /I "%INSTALL%"=="Y" (
        echo Installing AWS CLI...
        REM 使用Chocolatey安裝AWS CLI。如果未安裝Chocolatey，請先安裝它或改用其他安裝方法。
        choco install awscli
    ) else (
        echo AWS CLI installation skipped. Exiting...
        exit /b
    )
)

echo Configuring AWS CLI...
aws configure
echo AWS CLI configuration is complete.

