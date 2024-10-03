#!/bin/bash

# 請求用戶輸入版本號
read -p "Enter the version for the Docker image mishkan-frontend: " version

# 構建Docker映像
docker build --platform=linux/amd64 -t mishkan-frontend_v1:$version . --no-cache

# 登錄到AWS ECR
aws_login=$(aws ecr get-login-password --region ap-northeast-1)
docker login -u AWS -p "${aws_login}" 417696335634.dkr.ecr.ap-northeast-1.amazonaws.com

# 標記Docker映像
docker tag mishkan-backend:$version 417696335634.dkr.ecr.ap-northeast-1.amazonaws.com/mishkan-frontend_v1:$version

# 推送映像到ECR
docker push 417696335634.dkr.ecr.ap-northeast-1.amazonaws.com/mishkan-frontend_v1:$version

echo "Docker image mishkan-frontend:$version has been successfully pushed to AWS ECR."
