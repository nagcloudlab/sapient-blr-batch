pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "return-service"
        DOCKER_TAG = "latest"
        REGISTRY = "registry.internal.company.com"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/team/return-service.git'
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean package -DskipTests'
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker push ${REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}"
            }
        }

        stage('Deploy to Production') {
            steps {
                sh "kubectl apply -f k8s/deployment.yaml"
                sh "kubectl rollout status deployment/return-service --timeout=60s"
            }
        }
    }
}

// PROBLEMS (for training — do NOT reveal to students):
// 1. -DskipTests — tests are never run!
// 2. No test stage at all
// 3. Docker tag is always "latest" — no versioning/traceability
// 4. No security scanning (SonarQube, Trivy)
// 5. Deploys directly to production — no staging/canary
// 6. No rollback on failure
// 7. No approval gate before production deploy
// 8. No post-build cleanup
// 9. Credentials for registry not managed (no withCredentials)
// 10. No notifications on failure (Slack/email)
// 11. 60s rollout timeout may be too short for Spring Boot cold start
