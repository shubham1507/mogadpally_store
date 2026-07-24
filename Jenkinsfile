pipeline {

    agent {
        docker {
            image 'python:3.13-slim'
            reuseNode true
        }
    }

    options {
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Python Version') {
            steps {
                sh 'python --version'
                sh 'pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Django Check') {
            steps {
                sh '''
                    . venv/bin/activate
                    python manage.py check
                '''
            }
        }

    }

    post {
        success {
            echo 'Backend validation successful.'
        }

        failure {
            echo 'Backend validation failed.'
        }
    }
}