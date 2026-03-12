pipeline {
    agent any

    environment {
        PROJECT_ID = "ci-cd-pipeline-implementation"
        DOCKER_IMAGE = "vue-python-ci-cd-appliation"
        ARTIFACT_REPO = "aliassajucicdproject"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        CLUSTER_NAME = "vue-python-application-cluster"
        CLUSTER_ZONE = "us-central1-a"
        REGION = "us-central1"
        GAR_IMAGE = "${REGION}-docker.pkg.dev/${PROJECT_ID}/${ARTIFACT_REPO}/${DOCKER_IMAGE}:${IMAGE_TAG}"
        AWS_API_URL = "https://5fd40b51ke.execute-api.us-east-1.amazonaws.com/prod/metadata"
    }

    stages {

        stage('Clone Repo') {
            steps {
                git branch: 'main', credentialsId: 'GIT-JENKINS', url: 'https://github.com/as-aliassaju/smart-desk-assistant.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build --no-cache -t ${GAR_IMAGE} ."
            }
        }

        stage('Authenticate to GCP & Artifact Registry') {
            steps {
                sh '''
                gcloud config set project $PROJECT_ID
                gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                sh "docker push ${GAR_IMAGE}"
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

     stage('Send Metadata to AWS') {
    steps {
        withCredentials([string(credentialsId: 'AWS_API_KEY', variable: 'AWS_API_KEY')]) {
            sh """
            curl -X POST $AWS_API_URL \
            -H "Content-Type: application/json" \
            -H "x-api-key: $AWS_API_KEY" \
            -d '{ "pipeline":"$JOB_NAME", "status":"success", "build_id":"$BUILD_NUMBER" }'
            """
        }
    }
}

    }

    post {
        success {
            echo "✅ Build, push, Terraform, deployment, and AWS metadata logging completed successfully!"
        }
        failure {
            echo "❌ Build failed. Check logs."
        }
        always {
            echo "Finished build #${env.BUILD_NUMBER}"
        }
    }
}