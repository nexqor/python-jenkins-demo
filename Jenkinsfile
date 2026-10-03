pipeline {
    agent any

    environment {
        DEPLOY_DIR = '/opt/python-jenkins-demo'
        SERVICE_NAME = 'python-jenkins-demo'
    }

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

        stage('Deploy') {
            steps {
                sh '''
                    echo "Deploying application..."

                    mkdir -p "$DEPLOY_DIR/templates"
                    mkdir -p "$DEPLOY_DIR/static"

                    cp app.py "$DEPLOY_DIR/"
                    cp requirements.txt "$DEPLOY_DIR/"
                    cp templates/index.html "$DEPLOY_DIR/templates/"
                    cp static/style.css "$DEPLOY_DIR/static/"

                    echo "Application files deployed."
                '''
            }
        }

        stage('Restart Application') {
            steps {
                sh '''
                    echo "Restarting Gunicorn..."

                    systemctl restart "$SERVICE_NAME"

                    sleep 3

                    systemctl status "$SERVICE_NAME" --no-pager
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    echo "Checking application health..."

                    curl -f http://localhost:8000/health

                    echo ""
                    echo "Application is healthy!"
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
