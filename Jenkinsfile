/* groovylint-disable CompileStatic, DuplicateStringLiteral */
pipeline {
    agent any
    // parameters {
    //     choice(
    //         choices: ['only build' , 'build and push'],
    //         description: '',
    //         name: 'REQUESTED_ACTION')
    // }
    environment {
        REGISTRY = 'registry.gitlab.com/baltazar1697/tmtar_api'
    }
    stages {
        stage('BUILD') {
            agent any
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
                sh " docker build -t ${REGISTRY}:latest services/web/ "
                echo 'Building succeeded'
            }
        }
    
        stage('CODESTYLE-CHECK') {
            agent any
            steps {
                sh "docker build -f services/web/Dockerfile.test -t ${REGISTRY}:testing services/web/"
                sh "docker run ${REGISTRY}:testing "                
                echo 'Code checked'
            }
            // post {
            //     always {
            //         junit '*.json'
            //     }
            // }
        }
        stage('DB INIT & MIGRATE') {
            steps {
                sh 'docker-compose run web python manage.py db init'
                sh 'docker-compose run web python manage.py db migrate'
                sh 'docker-compose run web python manage.py db upgrade'
            }
        }
        stage('TESTS') {
            steps {
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
