pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "agdhanasekar/myapp"
        K8S_DEPLOYMENT = "myapp"
        K8S_CONTAINER = "myapp"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                checkout scm
                stash name: 'source-code', includes: '**/*'
            }
        }

        stage('Quality Checks') {
            parallel {

                stage('Lint') {
                    agent {
                        docker {
                            image 'python:3.11-slim'
                            args '-u root'
                            reuseNode true
                        }
                    }
                    steps {
                        unstash 'source-code'
                        sh 'pip3 install flake8 --quiet'
                        sh 'flake8 app.py --max-line-length=100'
                    }
                }

                stage('Unit Tests') {
                    agent {
                        docker {
                            image 'python:3.11-slim'
                            args '-u root'
                            reuseNode true
                        }
                    }
                    steps {
                        unstash 'source-code'
                        sh 'pip3 install -r requirements.txt --quiet'
                        sh 'pytest test_app.py -v --junitxml=test-results.xml'
                    }
                    post {
                        always {
                            junit 'test-results.xml'
                        }
                    }
                }

            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                sh "docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} ."
                sh "docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest"
                echo 'Image built and tagged successfully'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                    sh "docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                    sh "docker push ${DOCKER_IMAGE}:latest"
                    sh 'docker logout'
                }
                echo "Pushed ${DOCKER_IMAGE}:${BUILD_NUMBER} to Docker Hub"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Updating Kubernetes deployment with new image...'
                sh """
                    kubectl set image deployment/${K8S_DEPLOYMENT} \
                    ${K8S_CONTAINER}=${DOCKER_IMAGE}:${BUILD_NUMBER}
                """
                echo 'Waiting for rollout to complete...'
                sh "kubectl rollout status deployment/${K8S_DEPLOYMENT} --timeout=120s"
                echo 'Deployment successful!'
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Verifying pods are healthy...'
                sh 'kubectl get pods -l app=myapp'
                sh 'kubectl get deployment myapp'
                echo 'Waiting for all pods to be ready...'
                sh 'kubectl wait --for=condition=ready pod -l app=myapp --timeout=120s'
                echo 'All pods are ready and healthy!'
                sh 'kubectl rollout status deployment/myapp'
            }
        }

    }

    post {
        success {
            echo "Build ${BUILD_NUMBER} deployed successfully to Kubernetes."
        }
        failure {
            echo "Build ${BUILD_NUMBER} failed. Rolling back..."
            sh "kubectl rollout undo deployment/${K8S_DEPLOYMENT} || true"
            echo 'Rollback complete.'
        }
        always {
            sh "docker rmi ${DOCKER_IMAGE}:${BUILD_NUMBER} || true"
            echo 'Cleaned up local Docker image.'
        }
    }
}
