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
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
	    when {
		branch 'master'
		}
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
