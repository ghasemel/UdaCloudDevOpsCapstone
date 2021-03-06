# UdacityDevOpsCapstone
A simple inventory app to demonstrate following topics:

  * Working in AWS
  * Using Jenkins to implement Continuous Integration and Continuous Deployment
  * Building pipelines
  * Working with Ansible and CloudFormation to deploy clusters
  * Building Kubernetes clusters
  * Building Docker containers in pipelines

We used Blue/Green as the deployment strategy. 
At the last stage of the pipeline, after smoke test, 
we clean the old deployment (green).

Screenshots for all stages and steps of the pipeline 
have been provided in this repo. screenshots 01-08
Screenshots 09-12 provide the status on AWS console after success deployment.

The provided Makefile can be used for running different commands. 

## How to run:
    Run following commands from Makefile:
        > make setup
        > source ~/.venv/bin/activate
        > make install
        > add database configuration to database.ini file
            sample file: database-sample.ini
        > make [test_db_migration or prod_db_migration] # do the migration on database
        > python goods.py [test or prod]

## How to test:
    We use pytest to test the app
        > make test

## How to lint:
    To lint the app:
        > make lint

    To lint the Dockerfile
        > make lint-docker

## How to create/upload an Image/Container:
    All the required commands have been provided in run_docker.sh file
    We can run it like: ./run_docker.sh 
    in this way it will create the image and then run a container
    by passing 'basic' as the parameter, it does following actions:
        > build a image
        > run a container
        > stop the container
        > remove the container
    which can be use to test if everything has been correctly wrapped up

    To upload the image upload_docker.sh file can be used, first we need to provide the credentials of docker hub as below:
        > set environment variable $DOCKER_REPO_TOKEN for the token
        > change the username 'ghasemel' on line 17 to desired one

## How to create a cluster on AWS:
    We used eksctl tool to create the cluster on AWS, 
    it uses the CloudFormation template to create that, 
    all cloudformation templates are also included in the aws directory

    * cluster_eksctl.yaml can also be used to create the cluster by template
    * service_template.yaml used as the template for the pods on Kubernetes


## Tools/Frameworks:
    AWS
        * Elastic Kubernetes Service (EKS)
        * CloudFormation
        * eksctl
        * RDS (Postgres)
        * EC2
        * VPC
        * Subnet
    Python 3.7
        * Flask
        * Flask-Migrate
        * Flask-SQLAlchemy
        * Flask-Script
        * pytest
        * Flask-Testing
        * alchemy-mock
        * pylint
        * More in requirements.txt
    Docker
        * hadolint
    Kubernetes
    Jenkins
    Makefile
    
### Repository Link
https://github.com/ghasemel/UdaCloudDevOpsCapstone

