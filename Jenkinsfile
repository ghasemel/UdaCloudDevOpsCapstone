pipeline {
  agent {
    docker {
      image 'python:3.7.9'
    }

  }
  stages {
    stage('setup-env') {
      steps {
        sh '''ls
python3 -m venv .venv
. .venv/bin/activate
make install'''
      }
    }

  }
}