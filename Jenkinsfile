pipeline{
    agent {
        docker{
            image ' docker:stable '
            registryUrl 'registry.gitlab.com/baltazar1697/tmtar_api'
            //args  ' -v $HOME/.jcache'
            }
    environment {
        CI_REGISTRY_USER = 'baltazar1697'
        TOKEN = '2_DTzgQvcMT_9C_shZsD'
        }
    }
    stages {
        stage('Before build'){  
        
            steps {
                sh  '''
                    docker login -u $CI_REGISTRY_USER -p $TOKEN registry.gitlab.com
                    echo login successful
                    '''

                }
        }
        stage('Build') {
            steps {
                sh '''
                    export
                    docker pull registry.gitlab.com/baltazar1697/tmtar_api || true
                    docker build --cache-from registry.gitlab.com/baltazar1697/tmtar_api -t registry.gitlab.com/baltazar1697/tmtar_api:latest services/web/
                    docker push registry.gitlab.com/baltazar1697/tmtar_api:jlatest
                    echo login successful
                   '''
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
                sh 'echo flakehell checked '
            }
            post {
                always {
                    junit '*.json'
                }
            }
        }
        stage('Tests'){
            agent{
                docker{
                    sh ' apk add --no-cache docker-compose '
                    sh ' docker-compose -f docker-compose.test.yml up -d '

                }
            }
            step {

            }
            post {
                always {
                    junit '*.json'
                }
            }

        }
    }
    }
