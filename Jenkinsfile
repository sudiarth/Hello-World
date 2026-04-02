def getGitBranchName() {
    return scm.branches[0].name.split("/")[1]
}

pipeline {

  environment {
    GIT_BRANCH = getGitBranchName()
    DOCKER_REGISTRY_CREDENTIALS = credentials('AzureCredential')
    ACR_REGISTRY = "sudigitalacr.azurecr.io"
    IMAGE_NAME = "hello-world"
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
          sh "docker build -t ${ACR_REGISTRY}/${IMAGE_NAME}:${VERSION} ."
          sh 'echo $DOCKER_REGISTRY_CREDENTIALS_PSW | docker login $ACR_REGISTRY --username $DOCKER_REGISTRY_CREDENTIALS_USR --password-stdin'
          sh "docker push ${ACR_REGISTRY}/${IMAGE_NAME}:${VERSION}"
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
                    
                    sh "rm -rf '$repoDir'"

                    sh """
                        GIT_SSH_COMMAND="ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
                        git clone git@github.com:sudiarth/manifest.git '$repoDir'
                    """

                    dir("$repoDir") {
                        echo "Updating image tag in hello-world/values.yaml"
                        
                        sh "sed -i 's|hello-world:.*|hello-world:${VERSION}|g' hello-world/values.yaml"

                        sh 'git config --global user.email "sudieartha@gmail.com"'
                        sh 'git config --global user.name "sudiarth"'

                        sh 'git add hello-world/values.yaml'
                        
                        // Only commit and push if there are changes
                        def hasChanges = sh(script: 'git diff --cached --quiet', returnStatus: true)
                        if (hasChanges != 0) {
                            sh "git commit -m 'Update Image tag to ${VERSION}'"
                            sh """
                                GIT_SSH_COMMAND="ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
                                git push origin dev
                            """
                            echo "Manifest updated and pushed successfully"
                        } else {
                            echo "No changes to commit - tag already up to date"
                        }
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