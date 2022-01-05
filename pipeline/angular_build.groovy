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

                stage("Code Check Out") {
                    steps {
                        git branch: 'master', credentialsId: "${params.Credential_ID}", url: "${APP_URL}"
                        echo("${APP_URL} Repository was successfully cloned.")
                    }
                }

                stage("Install Node Modules") {
                    steps {
                        nodejs('Node') {
                            sh 'npm install'
                            sh 'npm install -g @angular/cli'
                            echo("Node Modules are installed successully")
                        }
                    }
                }

                stage('Build and SonarQube Code Analysis') {
                    steps{
                        script{
                            codeAnalysis.execAngularLinuxBuildAnalysis()
                        }
                    }
                }

                /*stage('Unit test application') {
                    //when { expression{ "${UnitTest}" == 'yes' } }
                    steps{
                        script
                        {
                            inspection.angularUnitTestApplication()
                        }
                    }
                }*/

                //Stage to Package the Artifacts
                stage('Package Deployment Artifacts') {
                    steps {
                        script {
                            // package artifacts with name 'package_name' and includes 'built code out put location folder ' 
                            dc_common.angularPackageArtifactsAll(Application_Name)
                        }
                    }
                }

                stage('Upload Deployment Artifact to S3') {
                    steps {
                        script {
                            s3_publish.angularUploadArtifactsToS3(Application_Name)
                        }
                    }
                }
            }
        }
    }

    options {
		timeout(time: 3, unit: 'MINUTES')   // timeout on whole pipeline job
		buildDiscarder(logRotator(numToKeepStr: env.branch == 'master' ? '' : "${buildsToKeep_final}"))
	}
}
