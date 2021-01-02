pipeline {
  agent {
    docker {
      image 'python:3.7.9'
    }

  }
  stages {
    stage('build') {
      steps {
        sh(script: '''pwd
ls -lah
make setup
. .venv/bin/activate
''', label: 'setup virtual environment')

        sh(script: '''ls -la
. .venv/bin/activate
make install''', label: 'install requirements')
      }
    }

  }
}