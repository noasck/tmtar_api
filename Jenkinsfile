pipeline {
    agent any
    environment {
        REGISTRY = 'registry.gitlab.com/baltazar1697/tmtar_api'
        USERNAME = 'baltazar1697'
        TOKEN = credentials('gitlab_reg_token')
    }
    stages {
        stage('LOGIN'){
            steps{
                sh " docker login -u ${USERNAME} -p ${TOKEN} ${REGISTRY}"
                echo '---------- LOGIN SUCCEED ----------'
            }
        }
        stage('BUILD') {
            agent any
            when {
                    branch 'master'
                }
            steps{
                
                sh " docker pull ${REGISTRY} "
                sh " docker build --cache-from ${REGISTRY} -f ./services/web/Dockerfile.prod -t ${REGISTRY}:prod_ready services/web/ "
                //sh " docker build -f ./services/web/Dockerfile.prod -t ${REGISTRY}:prod_ready services/web/ "
                sh " docker push ${REGISTRY}:prod_ready"
                echo '---------- BUILDING PROD IMAGE SUCCEED ----------'
            }
        }
        stage('UNIT TESTS'){
            when {
                    branch 'api_dev'
            }
            steps {
                sh 'docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit '
                echo '---------- TESTS SUCCEED ---------- '
            }
            post {
                failure {
                    junit './services/web/report.xml'
                }
            }
        }
        
        stage('PRODUCTION UP'){
            agent any
            when{
                    branch 'master'
                }
            steps{
                
                sh '''
                alias dc_down_test="docker-compose -f docker-compose.test.yml down"
                dc_down_test
                alias dc_build_prod="docker-compose -f docker-compose.prod.yml up --build"
                dc_build_prod -d 
                '''
                echo "DEPLOYED, MAN, IT'S READY"
            }
        }
    }
}
