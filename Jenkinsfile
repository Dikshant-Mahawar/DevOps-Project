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
         * 2️⃣ DEVSECOPS — Dockerfile Linting (Hadolint)
         * --------------------------------------------------------- */
        stage('Security Scan - Dockerfiles (Hadolint)') {
            steps {
                sh """
                echo '🔍 Running Hadolint security scan on Dockerfiles...'

                docker run --rm -i hadolint/hadolint < backend/Dockerfile  || true
                docker run --rm -i hadolint/hadolint < frontend/Dockerfile || true
                """
            }
        }

        /* ---------------------------------------------------------
         * 3️⃣ DEVSECOPS — Python SAST (Bandit in Virtual Env)
         * --------------------------------------------------------- */
        stage('Security Scan - Python Code (Bandit)') {
            steps {
                sh """
                echo '🔍 Running Bandit security scan on backend Python code...'

                # Create virtual environment (avoids system Python restriction)
                python3 -m venv bandit-venv
                . bandit-venv/bin/activate

                pip install --upgrade pip
                pip install bandit

                bandit -r backend/ -ll || true
                """
            }
        }

        /* ---------------------------------------------------------
         * 4️⃣ Docker Build & Push — COMMENTED OUT (Optional)
         * --------------------------------------------------------- */

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

        /* ---------------------------------------------------------
         * 5️⃣ Kubernetes Deployment
         * --------------------------------------------------------- */
        stage('Deploy to Kubernetes') {
            steps {
                echo "🚀 Deploying application to Kubernetes..."

                sh """
                kubectl apply -f k8s/backend-deployment.yaml
                kubectl apply -f k8s/frontend-deployment.yaml
                """
            }
        }
    }
}
