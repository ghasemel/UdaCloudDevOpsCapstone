pipeline {
  agent {
    docker {
      image 'python:3.7.9'
    }

  }
  stages {
    stage('install') {
      steps {
        sh '''ls
#python3 -m venv .venv
#source .venv/bin/activate
sudo make install'''
      }
    }

  }
}