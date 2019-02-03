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
		"${GIT_BRANCH}" == 'origin/master'
}

            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
		echo "${GIT_BRANCH}"
            }
        }
        
        }

	post {
	  always {
		cleanWs()
		}
	}
    }
