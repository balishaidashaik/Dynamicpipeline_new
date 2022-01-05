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
         
            stage('Code Check Out') {
               steps {
                  //git branch: '${Branch_Commit}', credentialsId: env.Credential_ID, url: '${APP_URL}'
                  echo("${APP_URL} Repository was successfully cloned.")
                  checkout([$class: 'GitSCM', branches: [[name: '*/${Branch_Commit}']], extensions: [], userRemoteConfigs: [[credentialsId: "${params.Credential_ID}", url: "${APP_URL}"]]])
               }
            }

            stage('Build') {
               steps{
                  script{
                     codeAnalysis.execDotnetLinuxBuildAnalysis("${FILE_NAME}")
                  }
               }
            }

            stage('Unit test application') {
               //when { expression{ "${UnitTest}" == 'yes' } }
               steps{
                  script {
                     inspection.dotnetUnitTestApplication()
                  }
               }
            }

            //Stage to Package the Artifacts
            stage('Package Deployment Artifacts') {
               steps {
                  script {
                        // package artifacts with name 'package_name' and includes 'built code out put location folder ' 
                        dc_common.dotnetPackageArtifactsAll("${FILE_NAME}")
                  }
               }
            }

            stage('Upload Deployment Artifact to S3') {
               steps {
                  script {
                        s3_publish.dotnetUploadArtifactsToS3("${FILE_NAME}")
                  }
               }
            }

            //Stage to upload the packaged artifacts to Nexus Repository
            /*stage('Upload Deployment Artifact to Nexus ') {
               steps {
                  script {
                        nexus.dotnetUploadArtifacts(Application_Name)
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
