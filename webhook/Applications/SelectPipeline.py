
class SelectPipelineScript:

    def selectpipeline(input):
            if input['ApplicationType'] == 'React':
                if input['BuildType'] == 'React_Build':
                    pipelinescript ='react_build.groovy'
                    return pipelinescript
                elif input['BuildType'] == 'React_Build_With_Test':
                    pipelinescript = 'react_build_with_test.groovy'
                    return pipelinescript
                elif input['BuildType'] == 'React_Build_With_Test_Gzip':
                    pipelinescript = 'react_build_with_test_gzip.groovy'
                    return pipelinescript
                else:
                    return False
            elif input['ApplicationType'] == 'Angular':
                if input['BuildType'] == 'Angular_Build':
                    pipelinescript ='angular_build.groovy'
                    return pipelinescript
                elif input['BuildType'] == 'Angular_Build_With_Test':
                    pipelinescript = 'angular_build_with_test.groovy'
                    return pipelinescript
                elif input['BuildType'] == 'Angular_Build_With_Test_Gzip':
                    pipelinescript = 'angular_build_with_test_gzip.groovy'
                    return pipelinescript
                else:
                    return False
            elif input['ApplicationType'] == 'Dotnet':
                pipelinescript ='dotnet.groovy'
                return pipelinescript
            elif input['ApplicationType'] == 'Spring':
                if input['BuildTool'] == 'Gradle':
                    pipelinescript ='spring_gradle.groovy'
                    return pipelinescript
                else:
                    pipelinescript ='spring_maven.groovy'
                    return pipelinescript
            else:
                return False

