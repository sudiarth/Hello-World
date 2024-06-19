def getGitBranchName() {
    return scm.branches[0].name.split("/")[1]
}

pipeline {

  environment {
    CONTAINER_REGISTRY_CREDENTIALS = credentials('AzureContainerRegistry')
    AWS_DEFAULT_REGION = 'ap-southeast-3'
    GIT_BRANCH = getGitBranchName()
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
          script {
            sh 'az --version'
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
