pipeline {
  agent {
    docker {
      image 'python:3.7.9'
      args '-u root:root'
      //args '-v /tmp/UdacityDevOpsCapstone:/var/lib/jenkins/workspace/UdacityDevOpsCapstone_main/~/.venv'
    }
  }


  stages {
    stage('build') {
      steps {
        //sleep(unit: 'HOURS', time: 1)
        sh(script: '''
          pwd
          ls -la
          make setup
          . ~/.venv/bin/activate
          ''', label: 'setup virtual environment')
        sh(script: '''
            ls -la
            . ~/.venv/bin/activate
            make install''', label: 'install requirements')

        sh(script: '''
          wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.19.0/hadolint-Linux-x86_64
          chmod 555 /bin/hadolint
          ''', label: 'install hadolint')
      }
    }

    stage('lint') {
      steps {
        sh(script: '''
          make lint-docker
          ''', label: 'Dockerfile lint')

        //sleep(unit: 'HOURS', time: 1)
        sh(script: '''
          . ~/.venv/bin/activate
          make lint
          ''', label: 'app lint')
      }
    }

    stage('test-db-migration') {
      steps {
        sh(script: '''
          echo "[postgresql-test]" > database.ini
          echo "host=$UDA_DB_HOST_TEST" >> database.ini
          echo "database=$UDA_DB_NAME" >> database.ini
          echo "user=$UDA_DB_USER_TEST" >> database.ini
          echo "password=$UDA_DB_PASS_TEST" >> database.ini
          echo "port=$UDA_DB_PORT_TEST" >> database.ini
          ''', label: 'Setup test database configuration')

        //sleep(unit: 'HOURS', time: 1)
        sh(script: '''
          . ~/.venv/bin/activate
          make db_migration_init
          make test_db_migration
          ''', label: 'run db migration on test database')
      }
    }

    stage('test') {
      steps {


        //sleep(unit: 'HOURS', time: 1)
        sh(script: '''
          . ~/.venv/bin/activate
          make test
          ''', label: 'run tests')
      }
    }
  }
}