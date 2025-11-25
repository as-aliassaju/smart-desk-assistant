pipeline {
    agent any

    environment {
        PROJECT_ID = "bubbly-mission-478719"
        DOCKER_IMAGE = "simple-reflex-simulator"
        IMAGE_TAG = "${env.BUILD_NUMBER}" // Unique tag per build
        GCR_IMAGE = "gcr.io/${PROJECT_ID}/${DOCKER_IMAGE}:${IMAGE_TAG}"
    }

    stages {
        stage('Clone Repo') {
            steps {
                echo "Cloning repository..."
                git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/as-aliassaju/smart-desk-assistant.git'
            }
        }

        stage('Authenticate to GCP') {
            steps {
                echo "Authenticating to GCP..."
                sh '''
                    gcloud auth activate-service-account --key-file=/var/lib/jenkins/gcloud-sa.json
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

        stage('Push Docker Image to GCR') {
            steps {
                echo "Pushing image to GCR..."
                sh "docker push ${GCR_IMAGE}"
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                echo "Stopping and removing old container if exists..."
                sh """
                    docker stop ${DOCKER_IMAGE} || true
                    docker rm ${DOCKER_IMAGE} || true
                """
            }
        }

        stage('Run Docker Container') {
            steps {
                echo "Running container ${DOCKER_IMAGE}..."
                sh "docker run -d --name ${DOCKER_IMAGE} ${GCR_IMAGE}"
            }
        }
    }

    post {
        success {
            echo "✅ Build + push + deployment completed successfully!"
        }
        failure {
            echo "❌ Build failed. Cleaning up..."
            sh """
                docker stop ${DOCKER_IMAGE} || true
                docker rm ${DOCKER_IMAGE} || true
            """
        }
        always {
            echo "Finished build #${env.BUILD_NUMBER}"
        }
    }
}
