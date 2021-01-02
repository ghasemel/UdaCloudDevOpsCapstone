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
        sh(script: '''wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.19.0/hadolint-Linux-x86_64
        ''', label: 'install hadolint')
        sh(script: '''
ls -la
. .venv/bin/activate
make lint
''', label: 'lint')

      }
    }


  }
}