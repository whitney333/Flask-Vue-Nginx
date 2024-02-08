Mishkan Project Intro
======================

it's an awesome project.!!! blah blah blah ...  


Development
============

frontend: blah blah blah ...  

backend: blah blah blah ...  


Deployment
==========


### 👩‍💻 Step 1 - install aws-cli tool and complete configure 

For Linux/Unix user:  

```
./aws_cli_config.sh  
```

For Windows user: 

powershell  

```
./win_aws_cli_config.ps1
``` 

CMD 

```
./win_aws_cli_config.bat
``` 

For further info, please visit AWS: https://docs.aws.amazon.com/zh_tw/cli/latest/userguide/getting-started-install.html

### 💾 Step 2 - docker-image build, tag, push and store in AWS ECR 

Just run:

```
./ready_for_deploy.sh
```

⚠️  Caution: frontend or backend version may not be the same. 


### 🤖 Step 3 - Use Github Action to trigger update 

1. tag current version of mishkan project

```
git tag $version
```

2. push tag to remote repo

```
git push --tag
```

This step will trigger github action to fetch the latest code of mishkan on EC2 and run docker-compose. The specific version of docker image will be deployed on EC2.  


### ⚙️  Maintain

*ECR side:*  More and more images would be stored on ECR repos. Some outdate images should be deleted in future.

*EC2 side:*  `docker image prune` was set in Github Action. It means Github Action will help us to remove all unmounted docker images.

*EC2 IP Address:*  If the EC2 instance is stopped, the original IP address will be lost. Consequently, the IP address in the ./github/workflow/aws.yml file will become invalid. Therefore, remember to update the corresponding IP address. If a static IP is assigned to the EC2 in the future, then you only need to enter that IP address in the aws.yml file.

*EC2 State:* 

If the EC2 instance is terminated, setting up a new EC2 instance will require the following essentials:

* Docker and docker-compose
* aws-cli

Moreover, if the EC2 is terminated, the GitHub Actions will also be invalidated. At this point, you will need to use ssh-keygen to generate a public key and a private key. The public key should be added to the ~/.ssh/authorized_keys on the EC2, and the private key should be stored in the GitHub Repo under Settings > Secrets and variables > Repository secrets.
