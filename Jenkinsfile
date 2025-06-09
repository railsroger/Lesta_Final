pipeline {
    agent any

    environment {
        // Docker configuration
        DOCKER_IMAGE = "${env.DOCKER_REGISTRY}/${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG}"
        
        // Credentials IDs (configure these in Jenkins)
        GITHUB_CREDENTIALS = 'github-credentials'
        DOCKER_REGISTRY_CREDENTIALS = 'docker-registry-credentials'
        DEPLOY_SSH_CREDENTIALS = 'deploy-ssh-key'
    }

    stages {
        stage('Checkout') {
            steps {
                // Clone repository using GitHub credentials
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    extensions: [],
                    userRemoteConfigs: [[
                        credentialsId: "${env.GITHUB_CREDENTIALS}",
                        url: 'git@github.com:railsroger/Lesta_Final.git'
                    ]]
                ])
            }
        }

        stages {
        stage('Checkout') {
            steps {
                sshagent(['github-credentials']) {
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            url: 'git@github.com:railsroger/Lesta_Final.git',
                            credentialsId: 'github-credentials'
                        ]]
                    ])
                }
            }
        }
    

        stage('Build') {
            steps {
                // Build Docker image
                sh '''
                    docker build -t ${DOCKER_IMAGE} .
                '''
            }
        }

        stage('Test/Lint') {
            parallel {
                stage('Lint') {
                    steps {
                        // Run flake8 for code linting
                        sh '''
                            docker run --rm ${DOCKER_IMAGE} flake8 .
                        '''
                    }
                }
                stage('Test') {
                    steps {
                        // Run pytest for testing
                        sh '''
                            docker run --rm ${DOCKER_IMAGE} pytest
                        '''
                    }
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    // Login to Docker Registry
                    withCredentials([usernamePassword(
                        credentialsId: "${env.DOCKER_REGISTRY_CREDENTIALS}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh '''
                            echo ${DOCKER_PASS} | docker login ${DOCKER_REGISTRY} -u ${DOCKER_USER} --password-stdin
                            docker push ${DOCKER_IMAGE}
                        '''
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Deploy using SSH
                    sshagent(['${env.DEPLOY_SSH_CREDENTIALS}']) {
                        // Create deployment directory if it doesn't exist
                        sh '''
                            ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} \
                                "mkdir -p ${DEPLOY_PATH}"
                        '''

                        // Copy necessary files to remote server
                        sh '''
                            scp -o StrictHostKeyChecking=no docker-compose.yml ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/
                            scp -o StrictHostKeyChecking=no .env ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/
                        '''

                        // Create and copy deployment script
                        writeFile file: 'deploy.sh', text: '''
                            #!/bin/bash
                            set -e

                            # Login to Docker Registry
                            echo ${DOCKER_PASS} | docker login ${DOCKER_REGISTRY} -u ${DOCKER_USER} --password-stdin

                            # Pull the latest image
                            docker pull ${DOCKER_IMAGE}

                            # Stop and remove existing containers
                            docker-compose down || true

                            # Start the new version
                            docker-compose up -d

                            # Clean up old images
                            docker image prune -f

                            # Logout from Docker Registry
                            docker logout ${DOCKER_REGISTRY}
                        '''

                        sh '''
                            chmod +x deploy.sh
                            scp -o StrictHostKeyChecking=no deploy.sh ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/
                        '''

                        // Execute deployment script on remote server
                        withCredentials([
                            usernamePassword(
                                credentialsId: "${env.DOCKER_REGISTRY_CREDENTIALS}",
                                usernameVariable: 'DOCKER_USER',
                                passwordVariable: 'DOCKER_PASS'
                            )
                        ]) {
                            sh '''
                                ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} \
                                    "cd ${DEPLOY_PATH} && \
                                    DOCKER_USER=${DOCKER_USER} \
                                    DOCKER_PASS=${DOCKER_PASS} \
                                    DOCKER_REGISTRY=${DOCKER_REGISTRY} \
                                    DOCKER_IMAGE=${DOCKER_IMAGE} \
                                    ./deploy.sh"
                            '''
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            // Cleanup
            sh '''
                docker logout ${DOCKER_REGISTRY} || true
                rm -f deploy.sh || true
            '''
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
} 
