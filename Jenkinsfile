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
          // sh "docker build -t helloworldsudigital.azurecr.io/hello-world:${VERSION} ."
          sh 'echo $DOCKER_REGISTRY_CREDENTIALS_PSW | docker login helloworldsudigital.azurecr.io --username $DOCKER_REGISTRY_CREDENTIALS_USR --password-stdin'
          sh "docker push helloworldsudigital.azurecr.io/hello-world:${VERSION}"
        }
      }
    }

    stage('Update Tag Manifest') {
      steps {
        container('docker') {
          withCredentials([sshUserPrivateKey(credentialsId: 'lanxic', keyFileVariable: 'SSH_KEY')]) {
            script {
              def repoDir = "${env.WORKSPACE}/manifest"
              try {
                // Clone the repository using SSH key into a specific directory
                sh "rm -rf '${repoDir}'"  // Clean up if the directory already exists
                sh "git clone git@github.com:sudiarth/manifest.git '$repoDir'"
                dir("$repoDir") {
                  echo 'Updating Image TAG'

                  // Update the image tag in the values.yaml file
                  sh "sed -i 's/hello-world:.*/hello-world:${VERSION}/g' hello-world/values.yaml"

                  echo 'Git Config'

                  // Set Git configurations
                  sh 'git config --global user.email "lanxic@gmail.com"'
                  sh 'git config --global user.name "lanxic"'

                  // Add changes
                  sh 'git add hello-world/values.yaml'

                  // Commit changes
                  sh "git commit -m 'Update Image tag to ${VERSION}'"

                  // Push changes to the master branch using the SSH key
                  sh "git push origin master"
                }
              } catch (Exception e) {
                echo "An error occurred: ${e.getMessage()}"
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
