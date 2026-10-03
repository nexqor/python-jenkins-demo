# Troubleshooting Guide

This document records the issues encountered while building and deploying the Python Flask application through Jenkins.

---

## 1. Virtual Environment Accidentally Pushed to GitHub

### Problem

The Python `venv/` directory was accidentally added to the Git repository.

A virtual environment should not normally be committed because it contains locally generated dependencies and can make the repository unnecessarily large.

### Solution

Added the following to `.gitignore`:

```gitignore
venv/
__pycache__/
*.pyc
.pytest_cache/
```

Then removed the already tracked virtual environment:

```bash
git rm -r --cached venv
```

Committed the change:

```bash
git add .gitignore
git commit -m "Remove virtual environment from repository"
git push origin main
```

---

## 2. Incorrect Flask Template Directory

### Problem

The project initially had:

```text
templates/
└── templates/
    └── index.html
```

Flask expected:

```text
templates/index.html
```

### Solution

Moved the file:

```bash
mv templates/templates/index.html templates/index.html
```

Removed the unnecessary directory:

```bash
rm -rf templates/templates
```

The final structure became:

```text
templates/
└── index.html
```

---

## 3. Incorrect Static Directory

### Problem

The CSS file was initially placed incorrectly:

```text
templates/static/style.css
```

Flask expects static files under:

```text
static/style.css
```

### Solution

Created the correct directory:

```bash
mkdir -p static
```

Moved the stylesheet:

```bash
mv templates/static/style.css static/style.css
```

Removed the incorrect directory:

```bash
rm -rf templates/static
```

Final structure:

```text
static/
└── style.css
```

---

## 4. Jenkins Permission Denied During Deployment

### Problem

The Jenkins pipeline failed during the deployment stage:

```text
mkdir: cannot create directory '/opt/python-jenkins-demo/templates':
Permission denied
```

Jenkins was running as the `jenkins` user and did not have permission to modify the deployment directory.

### Solution

Changed ownership:

```bash
sudo chown -R jenkins:jenkins /opt/python-jenkins-demo
```

After changing the ownership, Jenkins could create directories and copy application files.

### Result

The Deploy stage successfully executed:

```text
mkdir -p /opt/python-jenkins-demo/templates
mkdir -p /opt/python-jenkins-demo/static
cp app.py /opt/python-jenkins-demo/
cp requirements.txt /opt/python-jenkins-demo/
cp templates/index.html /opt/python-jenkins-demo/templates/
cp static/style.css /opt/python-jenkins-demo/static/
```

---

## 5. Jenkins Could Not Restart Gunicorn

### Problem

The deployment stage succeeded, but the Restart Application stage failed:

```text
Failed to restart python-jenkins-demo.service:
Interactive authentication required.
```

Jenkins was trying to execute:

```bash
systemctl restart python-jenkins-demo
```

but the `jenkins` user did not have permission to restart the systemd service.

---

## 6. Sudo Requested a Password

### Problem

The Jenkinsfile was changed to:

```bash
sudo -n /usr/bin/systemctl restart python-jenkins-demo
```

but Jenkins returned:

```text
sudo: a password is required
```

The `-n` option prevents sudo from asking for a password interactively.

### Solution

Created:

```text
/etc/sudoers.d/python-jenkins-demo
```

with:

```text
jenkins ALL=(root) NOPASSWD: /usr/bin/systemctl restart python-jenkins-demo
jenkins ALL=(root) NOPASSWD: /usr/bin/systemctl status python-jenkins-demo
```

Then validated:

```bash
visudo -c
```

---

## 7. Restart Worked but Status Failed

### Problem

The restart command eventually worked:

```text
sudo -n /usr/bin/systemctl restart python-jenkins-demo
```

However, Jenkins still failed at:

```bash
sudo -n /usr/bin/systemctl status python-jenkins-demo --no-pager
```

with:

```text
sudo: a password is required
```

### Cause

The sudoers rule allowed:

```text
/usr/bin/systemctl status python-jenkins-demo
```

but Jenkins was executing:

```text
/usr/bin/systemctl status python-jenkins-demo --no-pager
```

The command arguments did not match the sudoers rule exactly.

### Solution

Added the exact command to sudoers:

```text
jenkins ALL=(root) NOPASSWD: /usr/bin/systemctl status python-jenkins-demo --no-pager
```

Final configuration:

```text
jenkins ALL=(root) NOPASSWD: /usr/bin/systemctl restart python-jenkins-demo
jenkins ALL=(root) NOPASSWD: /usr/bin/systemctl status python-jenkins-demo
jenkins ALL=(root) NOPASSWD: /usr/bin/systemctl status python-jenkins-demo --no-pager
```

Validated:

```bash
visudo -c
```

Then tested:

```bash
sudo -u jenkins sudo -n /usr/bin/systemctl status python-jenkins-demo --no-pager
```

---

## 8. Final Successful Pipeline

After fixing the sudo configuration, the Jenkins pipeline completed successfully.

Final pipeline:

```text
Checkout
   ↓
Setup Python
   ↓
Install Dependencies
   ↓
Run Pytest
   ↓
Deploy Application
   ↓
Restart Gunicorn
   ↓
Health Check
   ↓
SUCCESS
```

Tests:

```text
2 passed
```

Health check:

```text
{"status":"healthy"}
```

---

## Useful Diagnostic Commands

### Check Jenkins user

```bash
id jenkins
```

### Check sudo permissions

```bash
sudo -l -U jenkins
```

### Validate sudoers

```bash
visudo -c
```

### Test command as Jenkins

```bash
sudo -u jenkins sudo -n /usr/bin/systemctl restart python-jenkins-demo
```

### Check service

```bash
systemctl status python-jenkins-demo --no-pager
```

### Check application

```bash
curl http://localhost:8000/
```

### Check health

```bash
curl http://localhost:8000/health
```

Expected:

```json
{"status":"healthy"}
```

### Check Gunicorn

```bash
ps aux | grep gunicorn
```

### Check service logs

```bash
journalctl -u python-jenkins-demo -n 50 --no-pager
```

---

## Troubleshooting Principle

When a Jenkins pipeline fails, identify the **first failing stage** rather than changing multiple stages at once.

For this project:

```text
Checkout       → Git problem
Setup Python   → Python/dependency problem
Test           → Application/test problem
Deploy         → File permission problem
Restart        → systemd/sudo problem
Health Check   → Application/network problem
```

This makes Jenkins CI/CD failures easier to isolate and fix.
