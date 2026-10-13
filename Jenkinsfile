pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps { checkout scm; sh 'ls -R . | head -30' }
    }
    stage('Build Docker image') {
      steps { sh 'docker build -t gemstore-app:${BUILD_NUMBER} app' }
    }
    stage('Run app in container') {
      steps {
        sh 'docker rm -f gemstore-app || true'
        sh 'docker run -d --name gemstore-app --network cicd -p 8081:80 gemstore-app:${BUILD_NUMBER}'
        sh 'sleep 3'
      }
    }
    stage('Selenium tests') {
      steps {
        sh 'docker build -t gemstore-tests tests'
        sh 'docker rm -f gemstore-tests || true'
        sh 'docker run --name gemstore-tests --network cicd -e APP_URL=http://gemstore-app gemstore-tests'
      }
      post {
        always {
          sh 'docker cp gemstore-tests:/tests/report.xml . || true'
          junit allowEmptyResults: true, testResults: 'report.xml'
          sh 'docker rm -f gemstore-tests || true'
        }
      }
    }
  }
}
