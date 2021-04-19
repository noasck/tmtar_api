/* groovylint-disable CompileStatic, DuplicateStringLiteral */
pipeline {
    agent any
    parameters {
        choice(
            choices: ['only build' , 'build and push'],
            description: '',
            name: 'REQUESTED_ACTION')
    }
    environment {
        REGISTRY = 'registry.gitlab.com/baltazar1697/tmtar_api'
    }
    stages {
        stage('Build') {
            agent {
                docker {
                    image ' docker:stable '
                    //registryUrl 'https://registry.gitlab.com/baltazar1697/tmtar_api'
                    //registryCredentialsId 'RegisrtyID'
                }
            }
            // when {
            //     expression { params.REQUESTED_ACTION == 'build and push' }
            // }
            // steps {
            //     sh 'docker login'
            //     echo 'login successful'
                
            //     sh 'docker pull ${REGISTRY}'
            //     sh 'docker build --cache-from registry.gitlab.com/baltazar1697/tmtar_api -t registry.gitlab.com/baltazar1697/tmtar_api:latest services/web/'
            //     sh 'docker push registry.gitlab.com/baltazar1697/tmtar_api:latest'
            //     echo 'build successful'
            // }
            steps{
                sh ' docker build -t ${env.BUILD_ID} services/web/ '
                echo 'Building succeeded'
            }
        }
    
        stage('FLAKEHELL') {
            agent {
                docker {
                    image ' python:3.7 '
                }
            }
            steps {
                sh 'pip3 install flakehell wemake-python-styleguide'
                sleep 30
                sh 'flakehell lint --format=gitlab --output-file flakehell.json'
                echo 'flakehell checked'
            }
            post {
                always {
                    junit '*.json'
                }
            }
        }
        stage('DB init & migrate') {
            steps {
                sh 'docker-compose run web python manage.py db init'
                sh 'docker-compose run web python manage.py db migrate'
                sh 'docker-compose run web python manage.py db upgrade'
            }
        }
        stage('Tests') {
            steps {
                sh 'apk add --no-cache docker-compose '
                sh 'docker-compose -f docker-compose.test.yml up -d '
            }
            post {
                always {
                    junit '*.xml'
                }
            }
        }
    }
}
