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
          sh "docker build -t helloworldsudigital.azurecr.io/hello-world:${VERSION} ."
          sh 'echo $DOCKER_REGISTRY_CREDENTIALS_PSW | docker login helloworldsudigital.azurecr.io --username $DOCKER_REGISTRY_CREDENTIALS_USR --password-stdin'
          sh "docker push helloworldsudigital.azurecr.io/hello-world:${VERSION}"
        }
      }
    }

    stage('Update Tag Manifest') {
      steps {
        script {
            def repoDir = "${env.WORKSPACE}/manifest"

            // Ensure VERSION is set
            if (!env.VERSION) {
                error "VERSION environment variable is not set. Aborting."
            }

            try {
                echo "Cloning manifest repository to ${repoDir}"
                echo "check ssh-key ${SSH_KEY}"
                
                // Clean up old repository if it exists
                sh "rm -rf '${repoDir}'"

                // Clone the repository
                sh "git clone git@github.com:sudiarth/manifest.git '${repoDir}'"

                // Change to repository directory
                dir("${repoDir}") {
                    echo "Updating image tag in hello-world/values.yaml"
                    
                    // Update the image tag in the values.yaml file
                    sh "sed -i 's/hello-world:.*/hello-world:${VERSION}/g' hello-world/values.yaml"

                    echo "Configuring Git for commits"
                    
                    // Set Git configurations
                    sh 'git config --global user.email "lanxic@gmail.com"'
                    sh 'git config --global user.name "lanxic"'

                    echo "Staging changes"
                    
                    // Stage and commit changes
                    sh 'git add hello-world/values.yaml'
                    sh "git commit -m 'Update Image tag to ${VERSION}'"

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
