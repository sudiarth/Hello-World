def getGitBranchName() {
    return scm.branches[0].name.split("/")[1]
}

pipeline {

  environment {
    AZURE_SUBSCRIPTION_ID='1a329798-f495-4d9c-8622-d52eac6b7169'
    AZURE_TENANT_ID='5def484d-a1e3-4154-b6f8-0eb8d4c41e13"'
    CONTAINER_REGISTRY='helloworldsudigital'
    RESOURCE_GROUP='sudigitalcluster-rg'
    REPO="hellow"
    IMAGE_NAME="hellow"
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
          withCredentials([usernamePassword(credentialsId: 'azure-cli-2024-06-17-13-49-37', passwordVariable: 'AZURE_CLIENT_SECRET', usernameVariable: 'AZURE_CLIENT_ID')]) {
            sh 'echo $AZURE_CLIENT_ID'
            sh 'echo $AZURE_CLIENT_SECRET'
            sh 'echo $AZURE_TENANT_ID'
            // sh 'az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET -t $AZURE_TENANT_ID'
            // sh 'az account set -s $AZURE_SUBSCRIPTION_ID'
            // sh 'az acr login --name $CONTAINER_REGISTRY --resource-group $RESOURCE_GROUP'
            // sh 'az acr build --image $REPO/$IMAGE_NAME:$TAG --registry $CONTAINER_REGISTRY --file Dockerfile . '
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
