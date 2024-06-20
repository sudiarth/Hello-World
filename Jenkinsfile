def getGitBranchName() {
    return scm.branches[0].name.split("/")[1]
}

pipeline {

  environment {
    GIT_BRANCH = getGitBranchName()
    DOCKER_REGISTRY_CREDENTIALS = credentials('AzureCredential')
    VERSION = "${env.BUILD_ID}"
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
          sh "docker build -t helloworldsudigital.azurecr.io/hello-world:latest ."
          sh 'echo $DOCKER_REGISTRY_CREDENTIALS_PSW | docker login helloworldsudigital.azurecr.io --username $DOCKER_REGISTRY_CREDENTIALS_USR --password-stdin'
          sh "docker push helloworldsudigital.azurecr.io/hello-world:latest"
        }
      }
    }

    stage('Restart Service') {
      steps {
        container('docker') {
          withCredentials([azureServicePrincipal('azure-principal-credential')]) {
            sh 'az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET -t $AZURE_TENANT_ID'
            sh 'az aks get-credentials --resource-group sudigitalcluster-rg --name sudigitalcluster-aks'
            sh 'kubectl version'
            sh 'kubectl rollout restart deployment hello-world -n ${GIT_BRANCH}'
          }
        }
      }
    }
  }
}
