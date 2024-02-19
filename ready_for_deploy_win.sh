# 請求用戶輸入前端版本號
$frontend_version = Read-Host -Prompt "Enter the version number for the mishkan-frontend deployment"

# 請求用戶輸入後端版本號
$backend_version = Read-Host -Prompt "Enter the version number for the mishkan-backend deployment"

# 使用 Out-File 命令創建 docker-compose-deploy.yml
@"
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
    image: "417696335634.dkr.ecr.ap-northeast-1.amazonaws.com/mishkan-frontend:$($frontend_version)"
    depends_on:
        - backend
    ports:
      - 8080:80
    restart: on-failure

  backend:
    image: "417696335634.dkr.ecr.ap-northeast-1.amazonaws.com/mishkan-backend:$($backend_version)"
    ports:
      - 5001:5001
    restart: on-failure
"@ | Out-File -FilePath docker-compose-deploy.yml -Encoding UTF8

Write-Host "docker-compose-deploy.yml has been created with frontend version $frontend_version and backend version $backend_version."

# 執行子目錄中的腳本並傳遞後端版本號作為參數
Write-Host "Executing build_and_push.sh in the backend directory with version $backend_version..."
Set-Location -Path .\backend
& .\build_and_push_win.sh $backend_version
Set-Location -Path ..

# 執行子目錄中的腳本並傳遞前端版本號作為參數
Write-Host "Executing build_and_push.sh in the frontend directory with version $frontend_version..."
Set-Location -Path .\frontend
& .\build_and_push_win.sh $frontend_version
Set-Location -Path ..

Write-Host "Complete deployment preparing. All images were sent to AWS ECR. Next step: use Github Action to trigger final update."

