pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                // Pull latest code from GitHub
                git credentialsId: 'github-token', url: 'https://github.com/as-aliassaju/simple_reflex_app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build Docker image from Dockerfile
                sh 'docker build -t simple-reflex-simulator .'
            }
        }

        stage('Run Docker Container') {
            steps {
                // Stop old container if exists, remove it, run new container
                sh '''
                    docker stop reflex-sim || true
                    docker rm reflex-sim || true
                    docker run -d --name reflex-sim simple-reflex-simulator
                '''
            }
        }
    }
}
