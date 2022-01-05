pipeline {
    agent any 

    stages {
        // CI stages 
        stage('Continuous Integration') {

            stages {

                stage('Initiation and clean up') {
                    steps {
                        echo 'Pre build validation and clean up workspace '
                        deleteDir()
                    }
                }
                //Stage to download the source code to Jenkins Build for compile/package
                stage('Checkout App Source Code') {
                    steps {
                        git branch: 'master', credentialsId: '${Credential_ID}', url: '${APP_URL}'
                        echo("${APP_URL} Repository was successfully cloned.")
                    }
                }

                stage ('Gradle Build') {
                    steps {
                        echo ("Building the Gradle application")
                        sh './gradlew build'
                        echo ("Gradle build is completed")
                    }
                }

                stage ('Code Analysis') {
                    steps {
                        withSonarQubeEnv('SonarQube') {
                            sh './gradlew sonarqube -Dsonar.host.url=http://3.21.88.185:9000'
                            echo ("Code analysis is completed by using SonarQube")
                        }
                    }
                }

                stage ('Gradle Test') {
                    steps {
                        echo 'Starting unit test execution'
                        sh './gradlew test'
                        echo 'Completed unit test execution'
                    }
                }

                stage ('Compressing the Artifacts') {
                    steps {
                        echo "Started Packaging artifacts"
                        sh 'zip -r "${Application_Name}.jar.zip" build/libs'
                        echo "Completed Packaging artifacts"
                    }      
                }

                stage ('Storing artifacts in nexus') {
                    steps {
                        echo "Started uploading artifacts to Nexus repository"
                        nexusArtifactUploader artifacts: [[artifactId: "${Application_Name}", classifier: '', file: '${Application_Name}.jar.zip', type: 'zip']], credentialsId: '27756e6f-60a1-4a35-bbc8-157d1ea67b68', groupId: 'org.example', nexusUrl: '3.142.21.161:8081', nexusVersion: 'nexus3', protocol: 'http', repository: 'gradle-repo', version: '4.0'
                        echo ("Artifacts are stored in the Nexus repository")
                    }
                }

                stage ('publish artifcats to s3') {
                    steps {
                        step ([
                            $class: 'S3BucketPublisher',
                            entries: [[
                                sourceFile: '${Application_Name}.jar.zip',
                                bucket: 'buildartifacts-dynamic-pipeline-jenkins',
                                selectedRegion: 'us-east-2',
                                noUploadOnFailure: true,
                                managedArtifacts: true,
                                //flatten: true,
                                showDirectlyInBrowser: true,
                                keepForever: true,
                            ]],
                            profileName: 'Dynamic-DevOps-Pipeline-Jenkins-S3',
                            dontWaitForConcurrentBuildCompletion: false,
                        ])
                        echo ("Artifacts are stored in the S3 bucket")
                    }
                }
            }
        }
    }
}