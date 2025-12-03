pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials-id'
        GITHUB_CREDENTIALS    = 'github-credentials-id'
        DOCKERHUB_USERNAME    = 'harsh4710'

        // ⭐ Add Minikube kubeconfig path for Kubernetes access
        KUBECONFIG = "/home/harsh-d/.kube/config"
    }

    stages {

        stage('Clone Repo') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Dikshant-Mahawar/DevOps-Project.git',
                        credentialsId: env.GITHUB_CREDENTIALS
                    ]]
                ])
            }
        }

        // ⭐⭐⭐ DEVSECOPS SECTION ⭐⭐⭐
        stage('Security Scan - Dockerfiles (Hadolint)') {
            steps {
                sh """
                echo '🔍 Running Hadolint security scan on Dockerfiles...'

                docker run --rm -i hadolint/hadolint < backend/Dockerfile || true
                docker run --rm -i hadolint/hadolint < frontend/Dockerfile || true
                """
            }
        }

        stage('Security Scan - Python Code (Bandit)') {
            steps {
                sh """
                echo '🔍 Running Bandit security scan on backend Python code...'
                pip install bandit
                bandit -r backend/ -ll || true
                """
            }
        }

        // ⭐⭐⭐ OPTIONAL — KEEP COMMENTED ⭐⭐⭐
        // stage('Build Backend Image') {
        //     steps {
        //         sh """
        //         docker build -t ${env.DOCKERHUB_USERNAME}/salon-backend:latest -f backend/Dockerfile .
        //         """
        //     }
        // }

        // stage('Build Frontend Image') {
        //     steps {
        //         sh """
        //         docker build -t ${env.DOCKERHUB_USERNAME}/salon-frontend:latest -f frontend/Dockerfile .
        //         """
        //     }
        // }

        // stage('Push Images to DockerHub') {
        //     steps {
        //         withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS,
        //                 usernameVariable: 'USER', passwordVariable: 'PASS')]) {
        //             sh """
        //             echo "$PASS" | docker login -u "$USER" --password-stdin
        //             docker push ${env.DOCKERHUB_USERNAME}/salon-backend:latest
        //             docker push ${env.DOCKERHUB_USERNAME}/salon-frontend:latest
        //             """
        //         }
        //     }
        // }

        // ⭐ Kubernetes Deployment Stage
        stage('Deploy to Kubernetes') {
            steps {
                echo "🚀 Applying Kubernetes manifests..."

                sh """
                kubectl apply -f k8s/backend-deployment.yaml
                kubectl apply -f k8s/frontend-deployment.yaml
                """
            }
        }
    }
}
