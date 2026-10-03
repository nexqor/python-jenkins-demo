pipeline {
    agent any

    stages {

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    echo "Python application build completed"
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    echo "Python application deployment started"
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    echo "Health check will run after deployment"
                '''
            }
        }
    }

    post {
        success {
            echo 'Python CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'Python CI/CD pipeline failed!'
        }
    }
}
