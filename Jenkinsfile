pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
    }

    environment {
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Lint') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --requirement requirements-dev.txt
                    .venv/bin/python -m compileall -q app.py aceest tests
                    .venv/bin/ruff check .
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '.venv/bin/pytest --junitxml=pytest-results.xml'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'pytest-results.xml'
                }
            }
        }

        stage('Docker Test Image') {
            steps {
                sh 'docker build --target test --tag aceest:test .'
                sh 'docker run --rm aceest:test'
            }
        }

        stage('Docker Runtime Image') {
            steps {
                sh 'docker build --target runtime --tag aceest:${BUILD_NUMBER} .'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'pytest-results.xml', allowEmptyArchive: true
        }
        success {
            echo 'ACEest BUILD and quality gate passed.'
        }
    }
}
