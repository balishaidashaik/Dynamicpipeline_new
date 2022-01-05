
timeout(20) {
  node("master") {
    stage("Code Check Out") {
    git branch: 'master', credentialsId: env.Credential_ID, url: '${APP_URL}'
    echo("${APP_URL} Repository was successfully cloned.")
    }
    stage ("Gradle Build") {    
      echo ("Gradle Build")
      sh './gradlew build'
    }
    stage ("Gradle Test") {     
      echo ("Gradle Test")
      sh './gradlew test'
    }
    stage ('Code Analysis') {
      withSonarQubeEnv('SonarQube') {
        sh './gradlew sonarqube -Dsonar.host.url=http://3.21.88.185:9000'
      }
    }
    stage ('zip Atifacts') {
        nodejs('Node') {
            sh 'zip -r "${Application_Name}.jar.zip" build/libs'
        }
    }
    stage ('Storing artifcats in nexus') {
        nexusArtifactUploader artifacts: [[artifactId: "${Application_Name}", classifier: '', file: '${Application_Name}.jar.zip', type: 'zip']], credentialsId: '27756e6f-60a1-4a35-bbc8-157d1ea67b68', groupId: 'org.example', nexusUrl: '3.142.21.161:8081', nexusVersion: 'nexus3', protocol: 'http', repository: 'gradle-repo', version: '4.0'
    }
    stage ("publish to s3") {
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
    }
    /*stage ('Pacakge Deployment Artifacts') {
      steps {
        echo "Started Packaging artifacts"
        powershell "Compress-Archive ${workspace}${BuildOutputLocation}\\* ${package_name} -Force"
        echo "Completed Packaging artifacts"
      }
    }
    stage ('Upload Deployment Artifact to Nexus') {
      steps {
        echo "Started uploading artifacts to Nexus repository"
        echo " upload file name : ${package_name} :"
        nexusArtifactUploader artifacts: [[artifactId: "${artifact_id}", file: "${package_name}", type: "${package_type}"]], credentialsId: "${nexus_credential}", groupId: "${nexus_groupID}", nexusUrl: "${nexus_URL}", nexusVersion: "${nexus_version}", protocol: "${nexus_protocol}", repository: "${nexus_repository}", version: "${artifact_version}"
        echo "Completed uploading artifacts to Nexus repository"
      }
    }
    stage("Gradle Version") {
      echo ("Gradle version")
      sh './gradlew -v'
    }
    stage ("Gradle Dependencies") {   
      echo ("Gradle Dependencies")
      sh './gradlew dependencies'
    }
    stage ("Gradle projects") {
      echo ("Displaying Gradle projects")
      sh './gradlew projects'
    }
    stage ("Gradle Task") {
      echo ("Displaying Gradle Task")
      sh './gradlew task'
    } 
    stage ('Archiving Artifacts') {
      echo ("Archiving Artifacts")
      archiveArtifacts artifacts: 'build/libs/*.jar', followSymlinks: false
    }
    stage ("Gradle Zip") {     
      echo ("Gradle Zip")
      sh 'gzip -r ./gradlew build'
    }
    stage ("Gradle Clean") {
      echo ("Cleaning Gradle Outputs")
      sh './gradlew clean'
    }
    stage ("Gradle Run") {   //Task 'run' not found in root project 'Transaction_0425'. Seems like no task are present to run
      echo ("Displaying Gradle Run Task")
      sh './gradlew run'
    } 
    stage ("Gradle Check") {     
      echo ("Displaying Gradle Check")
      sh './gradlew check'
    }*/
    echo("Spring Application is Built Successfully")
  }
}



//-----------------------------------------------------------


//--------------------------------------------------------------


timeout(5) {
  node("master") {
    stage("Code Check Out") {
      git branch: 'master', credentialsId: env.Credential_ID, url: '${APP_URL}'
      echo("${APP_URL} Repository was successfully cloned.")
    }
	
    stage("Build Node Modules") {
      nodejs('Node') {
      sh ' npm install sonarqube-scanner'
    }
      echo("Node Modules installed successully")
    }
	
    stage("Build/Package the Angular Application") {
      nodejs('Node') {
      sh 'npm run build'
      }
      echo("Build is completed")
    }
    /*stage ('Code Analysis') {
        nodejs('Node') {
            sh 'npm run sonar'
        }
      echo("Code Analysis is success")
    }*/
    stage ('Test') {
        nodejs('Node') {
            sh 'npm test'
        }
      echo("Test is completed")
    }
    stage ('zip dist') {
        nodejs('Node') {
            sh 'zip -r "dist.zip" dist/'
        }
    }
    stage ("publish to s3") {
      step ([
        $class: 'S3BucketPublisher',
        entries: [[
          sourceFile: 'dist.zip',
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
    }
    /*stage('Publish files to Nexus') {
        nexusArtifactUploader artifacts: [[artifactId: 'angular-helloworld', classifier: '', file: 'dist.zip', type: 'zip']], credentialsId: '27756e6f-60a1-4a35-bbc8-157d1ea67b68', groupId: 'com.angular', nexusUrl: '3.142.21.161:8081', nexusVersion: 'nexus3', protocol: 'http', repository: 'angular-repo', version: '5.0.0'
    }*/
      echo("Angular Application pipeline is created Successfully")
  }
}


//----------------------------------------------------------------------------------------

timeout(5) {
  node("master") {
    stage("Code Check Out") {
      git branch: 'master', credentialsId: env.Credential_ID, url: '${APP_URL}'
      echo("${APP_URL} Repository was successfully cloned.")
    }
	
    stage("Build Node Modules") {
      nodejs('Node') {
      sh 'npm install sonarqube-scanner'
    }
      echo("Node Modules installed successully")
    }
	
    stage("Build/Package the React Application") {
      nodejs('Node') {
      sh 'npm run build'
      }
      echo("Build is completed")
    }
    /*stage ('Code Analysis') {
        nodejs('Node') {
            sh 'npm run sonar'
        }
      echo("Code Analysis is success")
    }*/
    stage ('Test') {
        nodejs('Node') {
            sh 'npm test'
        }
      echo("Test is completed")
    }
    
    stage('Zip') {
        nodejs('Node') {
            sh 'zip -r "build.zip" build/'
        }
    }
    
    stage ("publish to s3") {
      step ([
        $class: 'S3BucketPublisher',
        entries: [[
          sourceFile: 'build.zip',
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
    }
    /*stage('Publish files to Nexus') {
        nexusArtifactUploader artifacts: [[artifactId: 'react-helloworld', classifier: '', file: 'build.zip', type: 'zip']], credentialsId: '27756e6f-60a1-4a35-bbc8-157d1ea67b68', groupId: 'com.react', nexusUrl: '3.142.21.161:8081', nexusVersion: 'nexus3', protocol: 'http', repository: 'react-repo', version: '1.0.0'
    }*/
      echo("React Application pipeline is created Successfully")
  }
}
