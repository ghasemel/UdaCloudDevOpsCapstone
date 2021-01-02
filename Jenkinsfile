pipeline {
  agent {
    docker {
      image 'python:3.7.9'
    }

  }
  stages {
    stage('setup-env') {
      steps {
        sh script: '''
pwd
ls -la
make setup
. .venv/bin/activate
make install''', label: "setup virtual environment"
      }
    }

  }
}
