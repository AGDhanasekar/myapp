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
