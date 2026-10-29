pipeline {
    agent any
    
    environment {
        DOCKER_HUB_USER = 'siddeadskull11' 
        IMAGE_NAME      = 'temp-converter'
        IMAGE_TAG       = "${env.GIT_COMMIT.substring(0,7)}" 
        DOCKER_CREDS    = credentials('docker-hub-credentials-id')
    }
    
    stages {
        stage('1. Continuous Integration (Pytest)') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install -r requirements.txt
                    pytest test_app.py
                '''
            }
        }
        
        stage('2. Build & Push Docker Image') {
            steps {
                bat "docker build -t %DOCKER_HUB_USER%/%IMAGE_NAME%:%IMAGE_TAG% ."
                bat "echo %DOCKER_CREDS_PSW% | docker login -u %DOCKER_CREDS_USR% --password-stdin"
                bat "docker push %DOCKER_HUB_USER%/%IMAGE_NAME%:%IMAGE_TAG%"
            }
        }
        
        stage('3. Deploy to Kubernetes') {
            steps {
                bat '''
                    powershell -Command "(Get-Content deployment.yaml) -replace 'DOCKERHUB_USERNAME/temp-converter:IMAGE_TAG', '%DOCKER_HUB_USER%/%IMAGE_NAME%:%IMAGE_TAG%' | Set-Content deployment.yaml"
                    kubectl apply -f deployment.yaml
                '''
            }
        }
    }
    
    post {
        always {
            bat "docker logout"
        }
    }
}