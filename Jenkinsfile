pipeline {
  agent none
  stages {
    stage('build') {
      agent {
        docker {
          image 'python:3.7.9-alpine'
          //args '-v $HOME/cache/UdacityDevOpsCapstone:/var/lib/jenkins/workspace/UdacityDevOpsCapstone_main/.venv'
        }

      }
      steps {
        sleep(unit: 'HOURS', time: 1)
        sh(script: '''
          pwd
          ls -la
          make setup
          . .venv/bin/activate
          ''', label: 'setup virtual environment')
        sh(script: '''
            ls -la
            . .venv/bin/activate
            make install''', label: 'install requirements')

      }
    }

    stage('lint') {
      agent {
        docker {
          image 'hadolint/hadolint'
        }

      }

      steps {
        sleep(unit: 'HOURS', time: 1)
        sh(script: '''
          ls -la
          . .venv/bin/activate
          make lint
          ''', label: 'lint')
      }
    }

  }
}