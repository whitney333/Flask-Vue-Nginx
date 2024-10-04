# Request the user to enter the version number
$version = Read-Host -Prompt "Enter the version for the Docker image mishkan-frontend"

# Build Docker image
docker build --platform linux/amd64 -t mishkan-frontend_v1:$version . --no-cache

# Login to AWS ECR
$aws_login = aws ecr get-login-password --region ap-northeast-1
docker login -u AWS -p $aws_login 417696335634.dkr.ecr.ap-northeast-1.amazonaws.com

# Tag Docker image
docker tag mishkan-frontend_v1:$version 417696335634.dkr.ecr.ap-northeast-1.amazonaws.com/mishkan-frontend_v1:$version

# Push image to ECR
docker push 417696335634.dkr.ecr.ap-northeast-1.amazonaws.com/mishkan-frontend_v1:$version

Write-Host "Docker image mishkan-frontend:$version has been successfully pushed to AWS ECR."

