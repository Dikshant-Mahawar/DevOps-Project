pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials-id'
        GITHUB_CREDENTIALS    = 'github-credentials-id'
        DOCKERHUB_USERNAME    = 'harsh4710'

        // kubeconfig for Minikube access
        KUBECONFIG = "/home/harsh-d/.kube/config"
    }

    stages {

        /* ---------------------------------------------------------
         * 1️⃣ Clone Repository
         * --------------------------------------------------------- */
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

        /* ---------------------------------------------------------
         * 2️⃣ Hadolint — Dockerfile Security Linting
         * --------------------------------------------------------- */
        stage('Security Scan - Dockerfiles (Hadolint)') {
            steps {
                sh """
                echo '🔍 Running Hadolint security scan on Dockerfiles...'

                docker run --rm -i hadolint/hadolint < backend/Dockerfile  || true
                docker run --rm -i hadolint/hadolint < frontend/Dockerfile || true
                docker run --rm -i hadolint/hadolint < supervisor/Dockerfile || true
        
                """
            }
        }

        /* ---------------------------------------------------------
         * 3️⃣ Trivy — Config Scan
         * --------------------------------------------------------- */
        stage('Security Scan - Trivy (Config Scan)') {
            steps {
                sh """
                echo '🔍 Running Trivy config scan on project YAML files...'

                docker run --rm -v ${env.WORKSPACE}:/project aquasec/trivy:latest config /project/k8s || true
                """
            }
        }

        /* ---------------------------------------------------------
         * 4️⃣ Bandit — Python SAST on Backend Code
         * --------------------------------------------------------- */
        stage('Security Scan - Python Code (Bandit)') {
            steps {
                sh """
                echo '🔍 Running Bandit security scan on backend Python code...'

                python3 -m venv bandit-venv
                . bandit-venv/bin/activate

                pip install --upgrade pip
                pip install bandit

                bandit -r backend/ -ll || true
                """
            }
        }

        /* ---------------------------------------------------------
         * 5️⃣ Docker Build & Push (Backend, Frontend, Supervisor)
         * --------------------------------------------------------- */

        stage('Build Images') {
            steps {
                sh """
                echo '🛠 Building Docker images...'

                docker build -t ${env.DOCKERHUB_USERNAME}/salon-backend:latest   -f backend/Dockerfile backend/
                docker build -t ${env.DOCKERHUB_USERNAME}/salon-frontend:latest  -f frontend/Dockerfile frontend/
                docker build -t ${env.DOCKERHUB_USERNAME}/supervisor-dashboard:latest -f supervisor/Dockerfile supervisor/
                """
            }
        }

        stage('Push Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS,
                        usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh """
                    echo "$PASS" | docker login -u "$USER" --password-stdin

                    docker push ${env.DOCKERHUB_USERNAME}/salon-backend:latest
                    docker push ${env.DOCKERHUB_USERNAME}/salon-frontend:latest
                    docker push ${env.DOCKERHUB_USERNAME}/supervisor-dashboard:latest
                    """
                }
            }
        }

        /* ---------------------------------------------------------
         * 6️⃣ Deploy to Kubernetes (Backend + Frontend + Supervisor + HPA + Ollama)
         * --------------------------------------------------------- */
        stage('Deploy to Kubernetes') {
            steps {
                sh """
                echo '🚀 Deploying application to Kubernetes...'

                # Backend
                kubectl apply -f k8s/backend-deployment.yaml
                kubectl apply -f k8s/backend-hpa.yaml

                # Frontend
                kubectl apply -f k8s/frontend-deployment.yaml

                # Supervisor Dashboard
                kubectl apply -f k8s/supervisor-dashboard.yaml

                # Ollama LLM Deployment (AI Layer)
                kubectl apply -f k8s/ollama-deployment.yaml

                echo "✅ All components deployed successfully!"
                """
            }
        }
    }
}