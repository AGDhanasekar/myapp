pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

        stage('Test') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root'
                    reuseNode true
                }
            }
            steps {
                echo 'Installing dependencies...'
                sh 'pip3 install -r requirements.txt'
                echo 'Running tests...'
                sh 'pytest test_app.py -v'
            }
        }

    }

    post {
        success {
            echo 'All stages passed! Build is successful.'
        }
        failure {
            echo 'Something failed. Check the logs above.'
        }
        always {
            echo 'Pipeline finished. This runs no matter what.'
        }
    }
}
