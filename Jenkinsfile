pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sleep 10
                sh 'mkdir dir_test'
            }
        }
        stage('Test') {
	    when {
		anyOf {
			branch "master";
			branch "origin/master"
}
}
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
		echo "${env.GIT_BRANCH}"
            }
        }
        
        }

	post {
	  always {
		cleanWs()
		}
	}
    }
