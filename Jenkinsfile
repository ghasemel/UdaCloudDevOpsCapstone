pipeline {

  agent none

  stages {
    // ******************************
    stage('build') {
      agent {
        docker {
          image 'python:3.7.9'
          args '-u root:root -v /tmp/UdacityDevOpsCapstone:/root/.venv'
        }
      }
      steps {
        //sleep(unit: 'HOURS', time: 1)
        sh(script: '''
          pwd
          ls -la
          make setup
          . ~/.venv/bin/activate
          ''', label: 'setup virtual environment')

        //sleep(unit: 'HOURS', time: 1)
        sh(script: '''
            ls -la
            . ~/.venv/bin/activate
            make install''', label: 'install requirements')
      }
    }

    // ******************************
    stage('lint') {
      agent {
        docker {
          image 'python:3.7.9'
          args '-u root:root -v /tmp/UdacityDevOpsCapstone:/root/.venv'
        }
      }
      steps {
        sh(script: '''
          wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.19.0/hadolint-Linux-x86_64
          chmod 555 /bin/hadolint
          ''', label: 'install hadolint')

        sh(script: '''
          make lint-docker
          ''', label: 'Dockerfile lint')

        //sleep(unit: 'HOURS', time: 1)
        sh(script: '''
          . ~/.venv/bin/activate
          make lint
          ''', label: 'Python lint')
      }
    }

    // ******************************
    stage('test') {
      agent {
        docker {
          image 'python:3.7.9'
          args '-u root:root -v /tmp/UdacityDevOpsCapstone:/root/.venv'
        }
      }

      steps {
        sh(script: '''
          echo "[postgresql-test]" > database.ini
          echo "host=$UDA_DB_HOST_TEST" >> database.ini
          echo "database=$UDA_DB_NAME" >> database.ini
          echo "user=$UDA_DB_USER_TEST" >> database.ini
          echo "password=$UDA_DB_PASS_TEST" >> database.ini
          echo "port=$UDA_DB_PORT_TEST" >> database.ini
          ''', label: 'set test-database configuration')

        // sleep(unit: 'HOURS', time: 1)
        sh(script: '''
          . ~/.venv/bin/activate
          make test_db_migration
          ''', label: 'migrate test database')

        sh(script: '''
          . ~/.venv/bin/activate
          make test
          ''', label: 'run tests')
      }

      post {
        always {
            echo 'clean up workspace'
            sh('rm -rf *')
            sh('rm -rf .pytest_cache')
        }
      }
    }

    // ******************************
    stage('build-image') {
      agent {
        docker {
          image 'eugenmayer/docker-client'
          args '-u root:root -v /var/run/docker.sock:/var/run/docker.sock'
        }
      }
      steps {
         sh(script: '''
          echo "[postgresql-prod]" > database.ini
          echo "host=$UDA_DB_HOST_PROD" >> database.ini
          echo "database=$UDA_DB_NAME" >> database.ini
          echo "user=$UDA_DB_USER_PROD" >> database.ini
          echo "password=$UDA_DB_PASS_PROD" >> database.ini
          echo "port=$UDA_DB_PORT_PROD" >> database.ini
          ''', label: 'create database.ini file')

        //sleep(unit: 'HOURS', time: 1)
        sh(script: '''
          ./run_docker.sh build
          ''', label: 'build docker image')

        sh(script: '''
          ./upload_docker.sh
          ''', label: 'upload docker image')
      }
    }


    // ******************************
    stage('migrate-database') {
      agent {
        docker {
          image 'python:3.7.9'
          args '-u root:root -v /tmp/UdacityDevOpsCapstone:/root/.venv'
        }
      }

      steps {
         sh(script: '''
          echo "[postgresql-prod]" > database.ini
          echo "host=$UDA_DB_HOST_PROD" >> database.ini
          echo "database=$UDA_DB_NAME" >> database.ini
          echo "user=$UDA_DB_USER_PROD" >> database.ini
          echo "password=$UDA_DB_PASS_PROD" >> database.ini
          echo "port=$UDA_DB_PORT_PROD" >> database.ini
          ''', label: 'set prod-database configuration')

        // sleep(unit: 'HOURS', time: 1)
        sh(script: '''
          . ~/.venv/bin/activate
          make prod_db_migration
          ''', label: 'run migration on prod database')
      }
      post {
        always {
            echo 'clean up workspace'
            sh('rm -rf *')
            sh('rm -rf .pytest_cache')
        }
      }
    }

    // ******************************
    stage('deploy') {
      agent {
        docker {
          image 'ubuntu:18.04'
          args '-u root:root'
        }
      }

      steps {
        sh(script: '''
          apt update -y
          apt install -y curl unzip less grep jq
          curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
          unzip awscliv2.zip
          ./aws/install
          aws --version

          export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
          export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
          export AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
          aws ec2 describe-instances \
            --query 'Reservations[*].Instances[*].{Instance:InstanceId}' \
            --output json

          curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
          chmod +x ./kubectl
          mv ./kubectl /usr/local/bin/kubectl
          kubectl version --client

          curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
          mv /tmp/eksctl /usr/local/bin
          eksctl version
          ''', label: 'install prerequisites')

        //sleep(unit: 'HOURS', time: 1)


        sh(script: '''
          cluster_name="inventory-cluster"
          eks_not_exist=$(aws cloudformation describe-stacks --stack-name eksctl-$cluster_name-cluster --query 'Stacks[*].StackId' 2>&1 | grep "does not exist" | wc -l)
          if [ $eks_not_exist -eq 1 ]; then
            eksctl create cluster \
                  --name $cluster_name \
                  --region us-west-2 \
                  --with-oidc \
                  --ssh-access \
                  --ssh-public-key udacity-key \
                  --managed
          else
            # config kubectl for eks if cluster already exist
            aws eks --region $AWS_DEFAULT_REGION update-kubeconfig --name $cluster_name
          fi

          # list all pods
          kubectl get pods --all-namespaces -o wide
          ''', label: 'deploy cluster - eks')

        sh(script: '''
          cd aws
          namespace="my-namespace-${BUILD_NUMBER}"

          # create pods template
          sed s/%MY_NAMESPACE%/$namespace/g \
            service_template.yaml > service.yaml

          kubectl create namespace $namespace
          kubectl apply -f service.yaml
          kubectl get all -n $namespace

          ''', label: 'deploy pods')

        sleep(unit: 'MINUTES', time: 3)

        sh(script: '''
          namespace="my-namespace-${BUILD_NUMBER}"

          kubectl get all -n $namespace

          loadbalancer_url=$(kubectl get services -n $namespace -o json | jq '.items[].status.loadBalancer.ingress[0].hostname' | cut -d '"' -f 2)
          echo $loadbalancer_url

          curl -H "Content-Type: text/plain" \
           -H "token: 452a712b-1375-4192-82e6-8e725b12dd9a" \
           --request PUT \
           --data $loadbalancer_url https://api.memstash.io/values/loadbalancer_url
        ''', label: 'save loadbalancer url')
      }
      post {
        always {
            echo 'clean up workspace'
            sh('rm -rf * || exit 0')
        }
      }
    }

    // ******************************
    stage('smoke-test') {
      agent {
        docker {
          image 'ubuntu:18.04'
          args '-u root:root'
        }
      }

      steps {
        sh(script: '''
          apt update -y
          apt install -y curl grep
          ''', label: 'install prerequisites')


        //sleep(unit: 'MINUTES', time: 5)
        sh(script: '''
          loadbalancer_url=$(curl -H "token: 452a712b-1375-4192-82e6-8e725b12dd9a" --request GET https://api.memstash.io/values/loadbalancer_url)
          echo "retrieved loadBalancer url: ${loadbalancer_url}"
          curl http://${loadbalancer_url}:8000/health > result.txt
          grep -i '"status": "ok"' result.txt
          ''', label: 'health endpoint')
      }

//       post {
//         always {
//             echo 'clean up workspace'
//             sh('rm -rf * || exit 0')
//         }
//       }
    }

    // ******************************
    stage('cleanup') {
      agent {
        docker {
          image 'ubuntu:18.04'
          args '-u root:root'
        }
      }

      steps {
        sh(script: '''
          apt update -y
          apt install -y curl unzip less grep jq
          curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
          unzip awscliv2.zip
          ./aws/install
          aws --version

          export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
          export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
          export AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
          aws ec2 describe-instances \
            --query 'Reservations[*].Instances[*].{Instance:InstanceId}' \
            --output json

          curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
          chmod +x ./kubectl
          mv ./kubectl /usr/local/bin/kubectl
          kubectl version --client

          curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
          mv /tmp/eksctl /usr/local/bin
          eksctl version

          # config kubectl for eks if cluster already exist
          cluster_name="inventory-cluster"
          aws eks --region $AWS_DEFAULT_REGION update-kubeconfig --name $cluster_name
          ''', label: 'install prerequisites')

        sh(script: '''
          # list all pods
          kubectl get pods --all-namespaces -o wide

          old=$(($BUILD_NUMBER-1))
          echo "old-namespace: ${old}"
          namespace="my-namespace-$old"
          kubectl delete ns $namespace

          ''', label: 'cleanup old namespace')

      }

      post {
        always {
            echo 'clean up workspace'
            sh('rm -rf * || exit 0')
        }
      }
    }
  }
}