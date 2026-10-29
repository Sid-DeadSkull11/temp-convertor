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
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest test_app.py
                '''
            }
        }
        
        stage('2. Build & Push Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "echo \$DOCKER_CREDS_PSW | docker login -u \$DOCKER_CREDS_USR --password-stdin"
                sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
        
        stage('3. Deploy to Kubernetes') {
            steps {
                sh """
                    sed -i 's|DOCKERHUB_USERNAME/temp-converter:IMAGE_TAG|${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}|g' deployment.yaml
                    kubectl apply -f deployment.yaml
                """
            }
        }
    }
    
    post {
        always {
            sh "docker logout"
        }
    }
}
