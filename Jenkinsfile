pipeline {
  agent none
  stages {
    stage('build') {
      agent {
        docker {
          image 'python:3.7.9'
          args '-v $HOME/cache/UdacityDevOpsCapstone:/tmp/.venv'
        }

      }
      steps {
        sh(script: '''
          pwd
          ls -la
          make setup
          . /tmp/.venv/bin/activate
          ''', label: 'setup virtual environment')
        sh(script: '''
            ls -la
            . /tmp/.venv/bin/activate
            make install''', label: 'install requirements')
        //sleep(unit: 'HOURS', time: 1)
      }
    }

    stage('lint') {
      agent {
        docker {
          image 'hadolint/hadolint'
        }

      }
      steps {
        sh(script: '''
          ls -la
          . /tmp/.venv/bin/activate
          make lint
          ''', label: 'lint')
      }
    }

  }
}