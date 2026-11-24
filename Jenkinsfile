pipeline {
    agent any

    environment {
        IMAGE_NAME   = 'lab11-site'
        STAGING_PORT = '8090'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'ls -l'
            }
        }

        stage('Build') {
            steps {
                sh '''
                    docker rm -f lab11-build || true
                    docker create --name lab11-build -w /app node:22-alpine sh -c "npm install && npm run build"
                    docker cp . lab11-build:/app
                    docker start -a lab11-build
                    rm -rf dist
                    docker cp lab11-build:/app/dist ./dist
                    docker rm -f lab11-build
                '''
            }
        }

        stage('Package') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Start Staging') {
            steps {
                sh '''
                    docker network create lab11-net || true
                    docker rm -f lab11-staging || true
                    docker run -d --name lab11-staging --network lab11-net -p ${STAGING_PORT}:80 ${IMAGE_NAME}:${BUILD_NUMBER}
                    sleep 3
                    docker exec lab11-staging wget -qO- http://localhost/ > /dev/null
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    docker build -t selenium-test-agent tests/
                    rm -f test-results.xml screenshot.png
                    docker rm -f lab11-test || true
                    docker create --name lab11-test --network lab11-net \
                        -e BASE_URL=http://lab11-staging -e HOME=/tmp \
                        selenium-test-agent pytest tests/test_site.py -v --junitxml=test-results.xml
                    docker cp tests lab11-test:/work/
                    STATUS=0
                    docker start -a lab11-test || STATUS=$?
                    docker cp lab11-test:/work/test-results.xml . || true
                    docker cp lab11-test:/work/screenshot.png . || true
                    docker rm -f lab11-test || true
                    exit $STATUS
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                    archiveArtifacts artifacts: 'screenshot.png', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'All tests passed. Deploying to production on port 80'
                sh '''
                    docker rm -f lab11-prod || true
                    docker run -d --name lab11-prod --restart unless-stopped -p 80:80 ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f lab11-staging || true'
        }
        success {
            echo "Build ${BUILD_NUMBER} deployed successfully"
        }
        failure {
            echo "Build ${BUILD_NUMBER} failed. Nothing new was deployed"
        }
    }
}
