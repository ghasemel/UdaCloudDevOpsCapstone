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
ls -la
make setup
. .venv/bin/activate
''', label: 'setup virtual environment')

        sh(script: '''ls -la
. .venv/bin/activate
make install''', label: 'install requirements')
      }
    }
    stage('lint') {
      steps {
        sh(script: '''
ls -la
. .venv/bin/activate
make lint
''', label: 'lint')

      }
    }


  }
}