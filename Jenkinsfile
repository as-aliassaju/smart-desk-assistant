pipeline {
    agent any

    environment {
        PROJECT_ID = "bubbly-mission-478719-h6"
        DOCKER_IMAGE = "simple-reflex-simulator"
        IMAGE_TAG = "${env.BUILD_NUMBER}" // Unique tag per build
        GCR_IMAGE = "gcr.io/${PROJECT_ID}/${DOCKER_IMAGE}:${IMAGE_TAG}"
        CLUSTER_NAME = "reflex-gke-cluster"
        CLUSTER_ZONE = "us-central1-a"
    }

    stages {

        stage('Clone Repo') {
            steps {
                git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/as-aliassaju/smart-desk-assistant.git'
            }
        }

        stage('Terraform Init & Apply') {
            steps {
                dir('terraform') {
                    sh '''
                        terraform init
                        terraform apply -auto-approve -var "project_id=${PROJECT_ID}" -var "region=${CLUSTER_ZONE}" -var "cluster_name=${CLUSTER_NAME}"
                    '''
                }
            }
        }

        stage('Authenticate to GCP & Docker') {
            steps {
                sh '''
                    gcloud config set project $PROJECT_ID
                    gcloud auth configure-docker gcr.io --quiet
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${GCR_IMAGE} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                sh "docker push ${GCR_IMAGE}"
            }
        }

        stage('Get GKE Credentials') {
            steps {
                sh "gcloud container clusters get-credentials $CLUSTER_NAME --zone $CLUSTER_ZONE --project $PROJECT_ID"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh "sed 's|{{IMAGE_TAG}}|${IMAGE_TAG}|g' k8s_deployment.yaml | kubectl apply -f -"
            }
        }
    }

    post {
        success { echo "✅ Build, push, Terraform, and deployment completed successfully!" }
        failure { echo "❌ Build failed. Check logs." }
        always { echo "Finished build #${env.BUILD_NUMBER}" }
    }
}
