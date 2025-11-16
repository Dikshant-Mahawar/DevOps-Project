pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials-id'
        GITHUB_CREDENTIALS    = 'github-credentials-id'
        DOCKERHUB_USERNAME    = 'harsh4710'
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

        stage('Build Backend Image') {
            steps {
                sh """
                docker build -t ${env.DOCKERHUB_USERNAME}/salon-backend:latest -f backend/Dockerfile .
                """
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh """
                docker build -t ${env.DOCKERHUB_USERNAME}/salon-frontend:latest -f frontend/Dockerfile .
                """
            }
        }

        stage('Push Images to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS,
                        usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh """
                    echo "$PASS" | docker login -u "$USER" --password-stdin
                    docker push ${env.DOCKERHUB_USERNAME}/salon-backend:latest
                    docker push ${env.DOCKERHUB_USERNAME}/salon-frontend:latest
                    """
                }
            }
        }
    }
}
