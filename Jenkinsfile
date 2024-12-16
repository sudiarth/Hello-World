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
          sh "docker build -t helloworldsudigital.azurecr.io/hello-world:$VERSION ."
          sh 'echo $DOCKER_REGISTRY_CREDENTIALS_PSW | docker login helloworldsudigital.azurecr.io --username $DOCKER_REGISTRY_CREDENTIALS_USR --password-stdin'
          sh "docker push helloworldsudigital.azurecr.io/hello-world:$VERSION"
        }
      }
    }

    stage('Update Tag Manifest') {
      steps {
        container('docker') {
          withCredentials([sshUserPrivateKey(credentialsId: 'jenkinsudi', keyFileVariable: 'SSH_KEY')]) {
            script {
                def repoDir = "${WORKSPACE}/manifest-repo"
                try {
                    echo "Cloning manifest repository to $repoDir"
                    
                    // Clean up old repository if it exists
                    sh "rm -rf '$repoDir'"

                    // Clone the repository
                    sh """
                        GIT_SSH_COMMAND="ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
                        git clone git@github.com:sudiarth/manifest.git '$repoDir'
                    """
                    // Change to repository directory
                    dir("$repoDir") {
                        echo "Updating image tag in hello-world/values.yaml"
                        
                        // Update the image tag in the values.yaml file
                        sh "sed -i 's/hello-world:.*/hello-world:$VERSION/g' hello-world/values.yaml"

                        echo "Configuring Git for commits"
                        
                        // Set Git configurations
                        sh 'git config --global user.email "sysadmin@cleanmedicindus.com"'
                        sh 'git config --global user.name "sysadmin"'

                        // Stage and commit changes
                        sh 'git add hello-world/values.yaml'
                        sh "git commit -m 'Update Image tag to $VERSION'"

                        echo "Pushing changes to master branch"
                        
                        // Push changes
                        sh "git push origin master"
                    }
                } catch (Exception e) {
                    echo "An error occurred while updating the manifest repository: ${e.getMessage()}"
                    currentBuild.result = 'FAILURE'
                    throw e
                }
            }
          }
        }
      }
    }
  }
}
