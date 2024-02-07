Mishkan Project Intro
======================

it's an awesome project.!!! blah blah blah ...  


Development
============

frontend: blah blah blah ...  

backend: blah blah blah ...  


Deployment
==========


### Step 1 - install aws-cli tool and complete configure 

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

### Step 2 - docker-image build, tag, push and store in AWS ECR 

Just run:

```
./ready_for_deploy.sh
```

⚠️  Caution: frontend or backend version may not be the same. 


### Step 3 - Use Github Action to trigger update 

1. tag current version of mishkan project

```
git tag $version
```

2. push tag to remote repo

```
git push --tag
```

This step will trigger github action to fetch the latest code of mishkan on EC2 and run docker-compose. The specific version of docker image will be deployed on EC2.  


### Maintain

ECR side: More and more images would be stored on ECR repos. Some outdate images should be deleted in future.

EC2 side: `docker image prune` was set in Github Action. It means Github Action will help us to remove all unmounted docker images.
