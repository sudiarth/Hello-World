def getGitBranchName() {
    return scm.branches[0].name.split("/")[1]
}

pipeline {

  environment {
    GIT_BRANCH = getGitBranchName()
    CONTAINER_REGISTRY_CREDENTIALS = credentials('AzureContainerRegistry')
    AWS_DEFAULT_REGION = 'ap-southeast-3'
    REGISTRY_NAME = "helloworldsudigital"
    REPOSITORY_NAME = "hellow"
    ACR_LOGIN_SERVER = "${REGISTRY_NAME}.azurecr.io"
  }
  
  agent {
    kubernetes {
      yaml '''
        apiVersion: v1
        kind: Pod
        spec:
          containers:
          - name: docker
            image: lanxic/docker-dind-aws-az-kubectl
            securityContext:
              privileged: true
        '''
    }
  }
  stages {
    stage('Get Branch Active'){
      steps {
        container('docker') {
          script {
            echo "${GIT_BRANCH}"
          }
        }
      }
    }

    stage('Build and Push Docker Image (dev)') {
      when {
        expression {
          GIT_BRANCH == 'dev'
        }
      }
      steps {
        container('docker') {
          // Building Docker Image 
          stage ('Build Docker image') {
              steps {
                  script {
                      sh "docker build -t ${REGISTRY_NAME}.azurecr.io/${REPOSITORY_NAME}:$BUILD_NUMBER ." 
                  }
              }
          }

          // Uploading Docker images into ACR
          stage('Upload Image to ACR') {
              steps{   
                  script {
                      withCredentials([usernamePassword(credentialsId: 'AzureContainerRegistry', usernameVariable: 'SERVICE_PRINCIPAL_ID', passwordVariable: 'SERVICE_PRINCIPAL_PASSWORD')]) {
                          sh "docker login ${ACR_LOGIN_SERVER} -u $SERVICE_PRINCIPAL_ID -p $SERVICE_PRINCIPAL_PASSWORD"
                          sh "docker push ${REGISTRY_NAME}.azurecr.io/${REPOSITORY_NAME}:$BUILD_NUMBER"
                      }
                  }
              }
          }
        }
      }
    }
    stage('Unsupported Branch') {
      when {
        expression {
          !(GIT_BRANCH == 'production' || GIT_BRANCH == 'dev')
        }
      }
      steps {
        error "Branch ${GIT_BRANCH} is not supported for building Docker image."
      }
    }
  }
}
