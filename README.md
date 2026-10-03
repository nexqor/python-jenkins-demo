# Python Jenkins CI/CD Demo

A production-style **Python Flask CI/CD pipeline using Jenkins**.

This project demonstrates how to automatically:

* Pull Python source code from GitHub
* Create a Python virtual environment
* Install project dependencies
* Run automated tests with Pytest
* Deploy the application to a Linux server
* Restart Gunicorn through systemd
* Perform an application health check
* Report the pipeline result through Jenkins

---

## Architecture

```text
                    GitHub
                       │
                       │
                       ▼
              ┌─────────────────┐
              │     Jenkins     │
              │                 │
              │  SCM Checkout   │
              │       ↓         │
              │  Python venv    │
              │       ↓         │
              │  Install deps   │
              │       ↓         │
              │     Pytest      │
              │       ↓         │
              │     Deploy      │
              └────────┬────────┘
                       │
                       │
                       ▼
              /opt/python-jenkins-demo
                       │
                       ▼
                 Gunicorn
                       │
                       ▼
                Flask Application
                       │
                       ▼
                 Port 8000
```

---

## CI/CD Pipeline

```text
GitHub
   │
   ▼
Checkout
   │
   ▼
Setup Python
   │
   ▼
Install Dependencies
   │
   ▼
Run Tests
   │
   ▼
Deploy Application
   │
   ▼
Restart Gunicorn
   │
   ▼
Health Check
   │
   ▼
Pipeline Success
```

---

## Technologies Used

| Technology | Purpose                        |
| ---------- | ------------------------------ |
| Python     | Application development        |
| Flask      | Web framework                  |
| Gunicorn   | WSGI application server        |
| Pytest     | Automated testing              |
| Jenkins    | CI/CD automation               |
| Git        | Version control                |
| GitHub     | Source code repository         |
| Linux      | Deployment server              |
| systemd    | Application service management |
| HTML/CSS   | Frontend                       |
| Bash       | Automation                     |

---

## Project Structure

```text
python-jenkins-demo/
│
├── Jenkinsfile
├── README.md
├── TROUBLESHOOT.md
├── app.py
├── requirements.txt
├── test_app.py
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── screenshots/
    ├── jenkins-pipeline-success.png
    ├── jenkins-test-success.png
    ├── application-homepage.png
    └── health-check.png
```

---

## Application

The Flask application provides two endpoints.

### Home

```text
/
```

Displays the project dashboard.

### Health Check

```text
/health
```

Returns:

```json
{
    "status": "healthy"
}
```

---

## Jenkinsfile

The Jenkins pipeline contains five main stages.

### 1. Setup Python

Creates a virtual environment and installs dependencies.

```groovy
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
```

### 2. Test

Runs the automated tests.

```groovy
stage('Test') {
    steps {
        sh '''
            source venv/bin/activate
            pytest
        '''
    }
}
```

### 3. Deploy

Copies the application files to the deployment directory.

```text
/opt/python-jenkins-demo
```

The pipeline deploys:

```text
app.py
requirements.txt
templates/index.html
static/style.css
```

### 4. Restart Application

Jenkins restarts the Gunicorn systemd service:

```bash
sudo -n /usr/bin/systemctl restart python-jenkins-demo
```

### 5. Health Check

Jenkins verifies that the application is responding:

```bash
curl -f http://localhost:8000/health
```

Expected result:

```json
{"status":"healthy"}
```

---

## Automated Tests

The project uses Pytest.

Run locally:

```bash
source venv/bin/activate
pytest
```

Expected result:

```text
2 passed
```

The tests verify:

* Home page returns HTTP 200
* Health endpoint returns the expected status

---

## Deployment

The application is deployed to:

```text
/opt/python-jenkins-demo
```

Gunicorn runs the Flask application on:

```text
0.0.0.0:8000
```

The systemd service is:

```text
python-jenkins-demo.service
```

Check the service:

```bash
sudo systemctl status python-jenkins-demo
```

Restart manually if required:

```bash
sudo systemctl restart python-jenkins-demo
```

---

## Jenkins Configuration

The Jenkins job uses:

```text
Pipeline script from SCM
```

Repository:

```text
https://github.com/nexqor/python-jenkins-demo.git
```

Branch:

```text
main
```

Jenkinsfile:

```text
Jenkinsfile
```

Jenkins automatically checks out the repository before executing the pipeline.

---

## Sudo Configuration

Jenkins needs permission to restart and check the application service without an interactive password prompt.

The configuration is stored in:

```text
/etc/sudoers.d/python-jenkins-demo
```

Example:

```text
jenkins ALL=(root) NOPASSWD: /usr/bin/systemctl restart python-jenkins-demo
jenkins ALL=(root) NOPASSWD: /usr/bin/systemctl status python-jenkins-demo
jenkins ALL=(root) NOPASSWD: /usr/bin/systemctl status python-jenkins-demo --no-pager
```

Validate the configuration:

```bash
visudo -c
```

Test as the Jenkins user:

```bash
sudo -u jenkins sudo -n /usr/bin/systemctl restart python-jenkins-demo
```

---

## Screenshots

### Jenkins Pipeline

Add your successful Jenkins pipeline screenshot here:

```text
screenshots/jenkins-pipeline-success.png
```

Example:

```markdown
![Jenkins Pipeline Success](screenshots/jenkins-pipeline-success.png)
```

### Automated Tests

```markdown
![Jenkins Tests](screenshots/jenkins-test-success.png)
```

### Application

```markdown
![Application Homepage](screenshots/application-homepage.png)
```

### Health Check

```markdown
![Health Check](screenshots/health-check.png)
```

---

## How to Run

### Clone the repository

```bash
git clone https://github.com/nexqor/python-jenkins-demo.git
cd python-jenkins-demo
```

### Create virtual environment

```bash
python3 -m venv venv
```

### Activate environment

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run tests

```bash
pytest
```

### Run Flask application

```bash
python app.py
```

The application will be available on:

```text
http://localhost:8000
```

---

## CI/CD Result

A successful Jenkins build performs the complete workflow automatically:

```text
Source Code
     ↓
GitHub
     ↓
Jenkins
     ↓
Python Environment
     ↓
Dependencies
     ↓
Automated Tests
     ↓
Deployment
     ↓
Gunicorn Restart
     ↓
Health Check
     ↓
SUCCESS
```

---

## Learning Outcomes

This project demonstrates practical experience with:

* Jenkins Declarative Pipeline
* CI/CD automation
* GitHub SCM integration
* Python virtual environments
* Automated testing
* Flask deployment
* Gunicorn
* Linux systemd services
* Linux permissions
* sudoers configuration
* Application health checks
* Troubleshooting Jenkins pipelines

---

## Author

**Manish Kumar**

GitHub: [@nexqor](https://github.com/nexqor)

Focus:

```text
AWS DevOps
Cloud Security
DevSecOps
CI/CD
Linux
Cloud Automation
```
