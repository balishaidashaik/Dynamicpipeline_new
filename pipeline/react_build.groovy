library 'shared-library'


node("master") 
{
  /*if ("${env.jenkins_slave_label}" != 'null') 
  {
    agent_label = "$jenkins_slave_label"
  }*/
  if (env.buildsToKeep)
  {
    buildsToKeep_final= env.buildsToKeep
  }
  else
  {
    buildsToKeep_final= '50'
  }
}


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
                        git branch: 'master', credentialsId: "${Credential_ID}", url: "${APP_URL}"
                        echo("${APP_URL} Repository was successfully cloned.")
                    }
                }

                stage("Install Node Modules") {
                    steps {
                        nodejs('Node') {
                            sh 'npm install'
                            echo("Node Modules are installed successully")
                        }
                    }
                }

                stage('Build and SonarQube Code Analysis') {
                    steps{
                        script{
                            codeAnalysis.execReactLinuxBuildAnalysis()
                        }
                    }
                }

                stage('Unit test application') {
                    //when { expression{ "${UnitTest}" == 'yes' } }
                    steps {
                        script {
                            inspection.reactUnitTestApplication()
                        }
                    }
                }

                //Stage to Package the Artifacts
                stage('Package Deployment Artifacts') {
                    steps {
                        script {
                            // package artifacts with name 'package_name' and includes 'built code out put location folder ' 
                            dc_common.reactPackageArtifactsAll(Application_Name)
                        }
                    }
                }

                stage('Upload Deployment Artifact to S3') {
                    steps {
                        script {
                            s3_publish.reactUploadArtifactsToS3(Application_Name)
                        }
                    }
                }

                //Stage to upload the packaged artifacts to Nexus Repository
                /*stage('Upload Deployment Artifact to Nexus ') {
                    steps {
                        script {
                            nexus.reactUploadArtifacts(Application_Name)
                        }
                    }
                }*/
            }
        }
    }

    options {
		timeout(time: 3, unit: 'MINUTES')   // timeout on whole pipeline job
		buildDiscarder(logRotator(numToKeepStr: env.branch == 'master' ? '' : "${buildsToKeep_final}"))
	}
}
