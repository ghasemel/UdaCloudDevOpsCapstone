pipeline {
  agent {
    docker {
      image 'python:3.7.9'
    }

  }
  stages {
    stage('setup-env') {
      steps {
        sh '''# setup virtual environment
pwd
ls -la
make setup
. .venv/bin/activate
make install'''
      }
    }

  }
}