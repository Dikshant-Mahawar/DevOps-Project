pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials-id'
        GITHUB_CREDENTIALS    = 'github-credentials-id'
        DOCKERHUB_USERNAME    = 'harsh4710'

        // kubeconfig for Minikube
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
                echo '🔍 Running Hadolint security scan...'

                docker run --rm -i hadolint/hadolint < backend/Dockerfile  || true
                docker run --rm -i hadolint/hadolint < frontend/Dockerfile || true
                docker run --rm -i hadolint/hadolint < supervisor/Dockerfile || true
                """
            }
        }

        /* ---------------------------------------------------------
         * 3️⃣ Trivy — YAML Config Scan
         * --------------------------------------------------------- */
        stage('Security Scan - Trivy (Config Scan)') {
            steps {
                sh """
                echo '🔍 Running Trivy config scan on Kubernetes files...'

                docker run --rm -v ${env.WORKSPACE}:/project \
                    aquasec/trivy:latest config /project/k8s || true
                """
            }
        }

        /* ---------------------------------------------------------
         * 4️⃣ Bandit — Python Backend Scan
         * --------------------------------------------------------- */
        stage('Security Scan - Python Code (Bandit)') {
            steps {
                sh """
                echo '🔍 Running Bandit SAST scan...'

                python3 -m venv bandit-venv
                . bandit-venv/bin/activate

                pip install --upgrade pip
                pip install bandit

                bandit -r backend/ -ll || true
                """
            }
        }

        // /* ---------------------------------------------------------
        //  * 5️⃣ Docker Build
        //  * --------------------------------------------------------- */
        // stage('Build Images') {
        //     steps {
        //         sh """
        //         echo '🛠 Building Docker images...'

        //         docker build -t ${env.DOCKERHUB_USERNAME}/salon-backend:latest   -f backend/Dockerfile backend/
        //         docker build -t ${env.DOCKERHUB_USERNAME}/salon-frontend:latest  -f frontend/Dockerfile frontend/
        //         docker build -t ${env.DOCKERHUB_USERNAME}/supervisor-dashboard:latest -f supervisor/Dockerfile supervisor/
        //         """
        //     }
        // }

        // /* ---------------------------------------------------------
        //  * 6️⃣ Docker Push
        //  * --------------------------------------------------------- */
        // stage('Push Images') {
        //     steps {
        //         withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS,
        //                 usernameVariable: 'USER', passwordVariable: 'PASS')]) {
        //             sh """
        //             echo "$PASS" | docker login -u "$USER" --password-stdin

        //             docker push ${env.DOCKERHUB_USERNAME}/salon-backend:latest
        //             docker push ${env.DOCKERHUB_USERNAME}/salon-frontend:latest
        //             docker push ${env.DOCKERHUB_USERNAME}/supervisor-dashboard:latest
        //             """
        //         }
        //     }
        // }

        // /* ---------------------------------------------------------
        //  * 7️⃣ Deploy to Kubernetes
        //  * --------------------------------------------------------- */
        // stage('Deploy to Kubernetes') {
        //     steps {
        //         sh """
        //         echo '🚀 Deploying microservices to Kubernetes...'

        //         # Backend + Autoscaler
        //         kubectl apply -f k8s/backend-deployment.yaml
        //         kubectl apply -f k8s/backend-hpa.yaml

        //         # Frontend
        //         kubectl apply -f k8s/frontend-deployment.yaml

        //         # Supervisor Dashboard
        //         kubectl apply -f k8s/supervisor-dashboard.yaml

        //         # Ollama Deployment
        //         kubectl apply -f k8s/ollama-deployment.yaml

        //         echo "✅ Kubernetes deployment complete!"
        //         """
        //     }
        // }

        /* ---------------------------------------------------------
         * 8️⃣ Start ELK Stack using Docker Compose
         * --------------------------------------------------------- */
        stage('Start ELK Stack') {
            steps {
                sh """
                echo '📊 Starting ELK Stack using Docker Compose...'

                cd elk
                docker compose down || true
                docker compose up -d

                echo '✅ ELK stack is up and running!'
                """
            }
        }

        /* ---------------------------------------------------------
         * 9️⃣ Deploy Filebeat to Kubernetes with Ansible
         * --------------------------------------------------------- */
        stage('Deploy Filebeat via Ansible') {
            steps {
                sh """
                echo '📦 Running Ansible playbook to deploy Filebeat...'

                cd ansible
                ansible-playbook -i inventory deploy-filebeat.yml

                echo '✅ Filebeat deployed with Ansible!'
                """
            }
        }
    }
}
