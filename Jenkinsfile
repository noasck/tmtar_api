/* groovylint-disable CompileStatic */
pipeline {
    agent none
    stages {
        stage('Before build') {
            agent {
                docker {
                    image ' docker:stable '
                    registryUrl 'registry.gitlab.com'
                    registryCredentialsId 'RegisrtyID'
                }
            }
            steps {
                sh 'docker login registry.gitlab.com'
                echo 'login successful'
            }
        }
        stage('Build') {
            steps {
                sh 'export'
                sh 'docker pull registry.gitlab.com/baltazar1697/tmtar_api || true'
                sh '''docker build --cache-from registry.gitlab.com/baltazar1697/tmtar_api
                -t registry.gitlab.com/baltazar1697/tmtar_api:latest services/web/
                '''
                sh 'docker push registry.gitlab.com/baltazar1697/tmtar_api:latest'
                echo 'build successful'
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
