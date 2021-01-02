pipeline {
  agent {
    node {
      label 'raouf'
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