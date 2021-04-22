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
            // }
            steps{
                sh " docker build -f services/web/Dockerfile.test -t ${REGISTRY}:testing services/web/ "
                echo '---------- Building testing image succeeded ----------'
            }
        }
        stage('TESTS') {
            parallel{
                stage('CODESTYLE-CHECK') {
                    agent any
                    steps {
                        sh "docker run ${REGISTRY}:testing "                
                        echo '---------- CODE CHECKED ----------'
                    }
                }
                stage('UNIT TESTS'){
                    steps {
                        sh 'docker-compose -f docker-compose.test.yml up --abort-on-container-exit '
                        echo '---------- TESTS SUCCEED---------- '
                    }
                
                    // post {
                    //     always {
                    //         junit '*.xml'
                    //     }
                    // }
                }
            }
        }
        stage('PRODUCTION UP'){
            agent any
            steps{
                sh '''
                alias dc_down_test="docker-compose -f docker-compose.test.yml down"
                dc_down_test
                alias dc_build_prod="docker-compose -f docker-compose.prod.yml up --build"
                dc_build_prod -d 
                '''
            }
        }
        stage('DB MIGRATIONS') {
            agent any
            steps {
                sh 'docker-compose run web python manage.py db migrate'
                sh 'docker-compose run web python manage.py db upgrade'
                echo '---------- DB MIGRATED ---------- '
            }
        }
    }
}
