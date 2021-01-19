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
          image 'amazon/aws-cli'
          args '-u root:root'
        }
      }

      steps {

        sh(script: '''
          echo test
          ''', label: 'test step')

        sleep(unit: 'HOURS', time: 1)


         sh(script: '''
          eksctl create cluster \
                --name inventory-cluster \
                --region us-west-2 \
                --with-oidc \
                --ssh-access \
                --ssh-public-key udacity-key \
                --managed
          ''', label: 'set prod-database configuration')

        // -${BUILD_NUMBER}


        sh(script: '''
          ''', label: 'run migration on prod database')
      }
      //post {
        //always {
            //echo 'clean up workspace'
            //sh('rm -rf *')
            //sh('rm -rf .pytest_cache')
        //}
      //}
    }
  }
}