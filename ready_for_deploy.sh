#!/bin/bash

# 請求用戶輸入前端版本號
read -p "Enter the version number for the mishkan-frontend deployment: " frontend_version

# 請求用戶輸入後端版本號
read -p "Enter the version number for the mishkan-backend deployment: " backend_version

# 使用cat命令創建docker-compose-deploy.yml
cat > docker-compose-deploy.yml <<EOF
version: '3'

services:

  # Proxies requests to internal services
  nginx:
    #1.17.10
    image: nginx:1.17.10
    container_name: t024-nginx
    depends_on:
        - frontend
        - backend
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    ports:
      - 80:80

  # generates frontend
  frontend:
    image: "417696335634.dkr.ecr.ap-northeast-1.amazonaws.com/mishkan-frontend:$frontend_version"
    depends_on:
        - backend
    ports:
      - 8080:80
    restart: on-failure

  backend:
    image: "417696335634.dkr.ecr.ap-northeast-1.amazonaws.com/mishkan-backend:$backend_version"
    ports:
      - 5001:5001
    restart: on-failure
EOF

echo "docker-compose-deploy.yml has been created with frontend version $frontend_version and backend version $backend_version."

# 執行子目錄中的腳本並傳遞後端版本號作為參數
echo "Executing build_and_push.sh in the backend directory with version $backend_version..."
(cd backend && ./build_and_push.sh "$backend_version")

# 執行子目錄中的腳本並傳遞後端版本號作為參數
echo "Executing build_and_push.sh in the backend directory with version $frontend_version..."
(cd frontend_rebuild && ./build_and_push.sh "$frontend_version")

echo "Complete deployment prepairing. All images were sent to AWS ECR. Next step: use Github Action to trigger final update."

