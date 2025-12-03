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
                echo '🔍 Running Trivy config scan on project...'

                docker run --rm -v ${env.WORKSPACE}:/project aquasec/trivy:latest config /project/backend   || true
                docker run --rm -v ${env.WORKSPACE}:/project aquasec/trivy:latest config /project/frontend  || true
                docker run --rm -v ${env.WORKSPACE}:/project aquasec/trivy:latest config /project/supervisor || true
                """
            }
        }

        /* ---------------------------------------------------------
         * 4️⃣ Bandit — Python SAST Security Scan
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
         * 5️⃣ Docker Build & Push (Backend + Frontend) — OPTIONAL
         * --------------------------------------------------------- */

        // stage('Build Backend Image') {
        //     steps {
        //         sh "docker build -t ${env.DOCKERHUB_USERNAME}/salon-backend:latest -f backend/Dockerfile ."
        //     }
        // }

        // stage('Build Frontend Image') {
        //     steps {
        //         sh "docker build -t ${env.DOCKERHUB_USERNAME}/salon-frontend:latest -f frontend/Dockerfile ."
        //     }
        // }

        // stage('Push Backend + Frontend Images') {
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
         * 6️⃣ Supervisor Dashboard — Build & Push
         * --------------------------------------------------------- */
        stage('Build Supervisor Image') {
            steps {
                sh """
                echo '🛠 Building Supervisor Dashboard image...'
                docker build -t ${env.DOCKERHUB_USERNAME}/supervisor-dashboard:latest \
                -f supervisor/Dockerfile supervisor/
                """
            }
        }

        stage('Push Supervisor Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS,
                        usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh """
                    echo "$PASS" | docker login -u "$USER" --password-stdin
                    docker push ${env.DOCKERHUB_USERNAME}/supervisor-dashboard:latest
                    """
                }
            }
        }

        /* ---------------------------------------------------------
         * 7️⃣ Kubernetes Deployment (Backend + Frontend + Supervisor)
         * --------------------------------------------------------- */
        stage('Deploy to Kubernetes') {
            steps {
                sh """
                echo '🚀 Deploying application to Kubernetes...'

                kubectl apply -f k8s/backend-deployment.yaml
                kubectl apply -f k8s/frontend-deployment.yaml
                kubectl apply -f k8s/supervisor-deployment.yaml
                """
            }
        }
    }
}
