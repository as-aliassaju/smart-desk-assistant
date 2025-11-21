pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "simple-reflex-simulator"
        CONTAINER_NAME = "reflex-sim"
        IMAGE_TAG = "${env.BUILD_NUMBER}" // Unique tag per build
    }

    stages {
        stage('Clone Repo') {
            steps {
                echo "Cloning repository..."
                git credentialsId: 'github-token', url: 'https://github.com/as-aliassaju/simple_reflex_app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${DOCKER_IMAGE}:${IMAGE_TAG}..."
                sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ."
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                echo "Stopping and removing old container if exists..."
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                """
            }
        }

        stage('Run Docker Container') {
            steps {
                echo "Running new container ${CONTAINER_NAME}..."
                sh "docker run -d --name ${CONTAINER_NAME} ${DOCKER_IMAGE}:${IMAGE_TAG}"
            }
        }
    }

    post {
        success {
            echo "Build completed successfully!"
        }
        failure {
            echo "Build failed. Cleaning up..."
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

