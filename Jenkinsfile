pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/nexqor/python-jenkins-demo.git'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
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
                    echo "Python application deployment completed"
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
