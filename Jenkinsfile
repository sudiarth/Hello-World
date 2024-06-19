def getGitBranchName() {
    return scm.branches[0].name.split("/")[1]
}

pipeline {

  environment {
    DOCKER_REGISTRY_CREDENTIALS = credentials('AzureCredential')
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
      steps {
        container('docker') {
          sh "docker build -t helloworldsudigital/hello-world:${VERSION} ."
          sh 'echo $DOCKER_REGISTRY_CREDENTIALS_PSW | docker login helloworldsudigital.azurecr.io --username $DOCKER_REGISTRY_CREDENTIALS_USR --password-stdin'
          sh "docker push helloworldsudigital/hello-world:${VERSION}"
        }
      }
    }
  }
}
