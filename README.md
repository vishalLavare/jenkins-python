# Jenkins Pipeline for Python Project Deployment

This guide outlines the steps to set up a Jenkins pipeline to build, test, and deploy a Python project. The pipeline pulls the code from Git, runs tests, and deploys it on a deployment server.

## Prerequisites
1. **Jenkins Setup**: Ensure Jenkins is installed and running.
2. **SSH Agent Plugin**:
   - Navigate to **Dashboard** -> **Manage Jenkins** -> **Plugin Manager** -> **Available Plugins**.
   - Search for `SSH Agent` and install it.
3. **SSH Credentials**:
   - Navigate to **Dashboard** -> **Manage Jenkins** -> **Credentials** -> **Global** -> **Add Credentials**.
   - Choose **Kind** as `SSH username with private key`.
   - Provide the username (e.g., `ubuntu`) and the private key (e.g., `.pem` key of the deployment server).

## Setting Up the Project
1. Create a local directory:
   ```bash
   mkdir pythonproject
   ```
2. Add the following files:
   - `requirements.txt`
   - `app.py`
   - `test_app.py`
3. Push the project to a GitHub repository.

## Preparing the Deployment Server
1. Launch a new server.
2. Install the required tools:
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip git
   ```
3. Create a directory and initialize Git:
   ```bash
   mkdir mypythonapp
   cd mypythonapp
   git init
   ```

## Creating the Jenkins Pipeline
1. Navigate to **Dashboard** -> **New Item** -> **Pipeline**.
2. Configure the pipeline:
   - Add a name and description.
   - Under **Build Triggers**, enable **GitHub hook triggers**.
   - Generate the pipeline syntax:
     - Go to **Pipeline Syntax** -> **Checkout from Version Control**.
     - Paste the GitHub repository URL and select the branch.
     - Copy the generated script.
3. Use the following pipeline script:

```groovy
pipeline {
    agent any

    stages {
        stage('git clone') {
            steps {
                echo 'Clone the GitHub repository'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/vishalLavare/jenkins-python.git']])
            }
        }
        stage('Build') {
            steps {
                echo 'Build Python project'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Test Python project'
                sh '''
                    . venv/bin/activate
                    python -m unittest discover -s test -p "test.py"
                '''
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploy Python project'
                script {
                    sshagent(['8636044c-8504-49d1-aa71-e8ad9df72ba6']) {  // ID of the SSH credential
                        sh '''
                            ssh -o StrictHostKeyChecking=no ubuntu@34.239.127.242 << EOF
                            cd /home/ubuntu/pythonproj || { echo "Deployment directory does not exist. Exiting..."; exit 1; }
                            git pull https://github.com/vishalLavare/jenkins-python.git
                            pip install -r requirements.txt
                            gunicorn --bind 0.0.0.0:5000 app:app &
                            exit
                            EOF
                        '''
                    }
                }
            }
        }
    }
}
```

## Key Notes
- Replace `mypython` with the name of your Python tool in Jenkins.
- Replace `8636044c-8504-49d1-aa71-e8ad9df72ba6` with your SSH credential ID.
- Replace `34.239.127.242` with your deployment server's public IP address.
- Ensure the deployment server directory (`/home/ubuntu/pythonproj`) exists and is initialized with Git.

## Author
[Vishal Lavare](https://github.com/vishalLavare)


