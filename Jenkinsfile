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
	    when { env.BRANCH == 'master' }
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
		echo "${env.BRANCH}"
            }
        }
        
        }

	post {
	  always {
		cleanWs()
		}
	}
    }
