pipeline {
  agent {
    docker {
      image 'python:3.7.9'
    }

  }
  stages {
    stage('setup-env') {
      steps {
        sh(script: '''pwd
ls -lah
make setup
. .venv/bin/activate
''', label: 'setup virtual environment')
      }
    }

    stage('error') {
      steps {
        sh 'make install'
      }
    }

  }
}