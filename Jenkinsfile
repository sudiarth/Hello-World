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

    stage('Update Manifest') {
        steps {
            script {
                def repoDir = "${env.WORKSPACE}/manifest"
                withCredentials([sshUserPrivateKey(credentialsId: jenkins, keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                      eval "$(ssh-agent -s)"
                      ssh-add $SSH_KEY
                      mkdir -p ~/.ssh
                      echo -e "Host github.com\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config
                      git clone git@github.com:sudiarth/manifest.git ''' + repoDir + '''
                      cd ''' + repoDir + '''
                      echo "Updating Image TAG - $VERSION"
                      sed -i 's/hello-world:.*/hello-world:$VERSION/g' hello-world/values.yaml
                      echo "Git Config"
                      git config --global user.email "lanxic@gmail.com"
                      git config --global user.name "lanxic"
                      git add hello-world/values.yaml
                      git commit -m "Update Image tag to $VERSION"
                      git push origin master
                      '''
                }
            }
        }
    }
  }
}
