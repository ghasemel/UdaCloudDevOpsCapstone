pipeline {
  agent {
    docker {
      image 'python:3.7.9'
    }

  }
  stages {
    stage('setup-env') {
      steps {
        sh '''pwd
ls -la
make setup
make install'''
      }
    }

  }
}