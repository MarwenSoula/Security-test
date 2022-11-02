
pipeline {
  agent any
  stages {
    stage('version') {
      steps {
        sh 'python3 --version'
      }
    }
    stage('Importing') {
      steps {
        sh 'python3 Prod-Engage.py'
      }
    }
  }
}
