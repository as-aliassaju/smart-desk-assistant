pipeline {
    agent any

    environment {
        PROJECT_ID = "bubbly-mission-478719-h6"
        DOCKER_IMAGE = "simple-reflex-simulator"
        IMAGE_TAG = "${env.BUILD_NUMBER}" // Unique tag per build
        GCR_IMAGE = "gcr.io/${PROJECT_ID}/${DOCKER_IMAGE}:${IMAGE_TAG}"
        CONTAINER_NAME = "reflex-sim"
    }

    stages {

        stage('Clone Repo') {
            steps {
                echo "Cloning repository..."
                git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/as-aliassaju/smart-desk-assistant.git'
            }
        }

        stage('Prepare Docker/GCR') {
            steps {
                echo "Configuring Docker to push to GCR..."
                sh '''
                    gcloud config set project $PROJECT_ID
                    gcloud auth configure-docker gcr.io --quiet
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${DOCKER_IMAGE}:${IMAGE_TAG}..."
                sh "docker build -t ${GCR_IMAGE} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "Pushing Docker image to GCR..."
                sh "docker push ${GCR_IMAGE}"
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                echo "Stopping old container if exists..."
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                """
            }
        }

        stage('Run Docker Container') {
            steps {
                echo "Running new container ${CONTAINER_NAME}..."
                sh "docker run -d --name ${CONTAINER_NAME} ${GCR_IMAGE}"
            }
        }
    }

    post {
        success {
            echo "✅ Build, push, and deployment completed successfully!"
        }
        failure {
            echo "❌ Build failed. Cleaning up..."
            sh """
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
            """
        }
        always {
            echo "Finished build #${env.BUILD_NUMBER}"
        }
    }
}
