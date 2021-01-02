pipeline {
  agent {
    docker {
      image 'python:3.7.9'
    }

  }
  stages {
    stage('install') {
      steps {
        sh 'make install'
      }
    }

  }
}