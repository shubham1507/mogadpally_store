pipeline {

    agent any

    options {
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Environment') {
            steps {
                sh 'pwd'
                sh 'ls -la'
                sh 'python3 --version || true'
                sh 'pip3 --version || true'
            }
        }
    }

    post {
        success {
            echo 'Environment verification successful.'
        }
    }
}