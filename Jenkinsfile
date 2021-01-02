pipeline {
  agent {
    docker {
      args '3.7.9'
      image 'python'
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