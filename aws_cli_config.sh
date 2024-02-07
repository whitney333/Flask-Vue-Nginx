#!/bin/bash

# 檢查是否安裝了 aws-cli
if ! command -v aws &> /dev/null; then
    echo "aws-cli could not be found. Please install it."
    # 根據您的系統選擇合適的安裝命令
    # 以下是在Debian/Ubuntu上安裝aws-cli的示例
    read -p "Do you want to install aws-cli now? (y/n): " answer
    if [[ "$answer" = "y" ]]; then
        # 使用curl下載安裝腳本並執行
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        unzip awscliv2.zip
        sudo ./aws/install
        # 檢查安裝是否成功
        if ! command -v aws &> /dev/null; then
            echo "Installation failed. Please install aws-cli manually."
            exit 1
        fi
    else
        echo "aws-cli is required to proceed."
        exit 1
    fi
fi

echo "aws-cli is installed."
# 執行aws configure
echo "Please enter your AWS credentials."
aws configure

