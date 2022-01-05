import flask,json,os,logging
from ruamel.yaml import YAML


from Applications.CommonFunctions import CommonFunctions
from Applications.SelectPipeline import SelectPipelineScript

app = flask.Flask(__name__)
app.config["DEBUG"] = True
yaml=YAML()
with open('./config.json') as f:
    config=json.load(f)
    
path = config['default_home_path']

class SpringApplication:

    def createspringjob(input,apprepo):
        pipeline_repo_path=os.path.join(path,config['repo_name'])
        if os.path.isdir(pipeline_repo_path):
            logging.info("Pulling the Main repository")
            CommonFunctions.gitpull(pipeline_repo_path)
            if input['BuildTool'] == 'Gradle':
                logging.info('Calling Spring job subcreation function using Gradle')
                return SpringApplication.subcreatespringgradlejob(pipeline_repo_path,apprepo,input)
            else:
                logging.info('Calling Spring job subcreation function using Maven')
                return SpringApplication.subcreatespringmavenjob(pipeline_repo_path,apprepo,input)
        else:
            logging.info("Cloning the Main repository")
            CommonFunctions.gitclone(path,config['job_git_url'])
            if input['BuildTool'] == 'Gradle':
                logging.info('Calling Spring job subcreation function using Gradle')
                return SpringApplication.subcreatespringgradlejob(pipeline_repo_path,apprepo,input)
            else:
                logging.info('Calling Spring job subcreation function using Maven')
                return SpringApplication.subcreatespringmavenjob(pipeline_repo_path,apprepo,input)


    def subcreatespringgradlejob(pipeline_repo_path,apprepo,input):
        try: 
            yamlpath=os.path.join(pipeline_repo_path,"jobs/springgradlejob.yaml")
            yamlcontent=CommonFunctions.readyaml(yamlpath)
            logging.info("Selecting the Spring Pipeline Script using Gradle")
            pipelinescript=SelectPipelineScript.selectpipeline(input)
            pipelinefile=os.path.join(pipeline_repo_path,"pipeline/",pipelinescript)
            if os.path.exists(pipelinefile) and os.path.getsize(pipelinefile) > 0:
                modifiedyaml=SpringApplication.modifyyamlforspringgradle(yamlcontent,input,apprepo,pipelinescript)
                logging.info("Modifying the Spring Gradle Yaml file based on the Developer inputs")
                if(CommonFunctions.writeyaml(modifiedyaml,'./springgradlejob.yaml')):
                    os.system('jenkins-jobs --conf ./jenkins_jobs.ini update ./springgradlejob.yaml')
                    logging.info('Spring job is created using Gradle')
                    return ('Spring job is created using Gradle')
                else:
                    return ('Error in writing Spring Gralde yaml file')
            #else:
             #   return ('Spring Gradle Pipelinescript is empty')
        except Exception as e:
           logging.info(e)

    def subcreatespringmavenjob(pipeline_repo_path,apprepo,input):
        try:
            yamlpath=os.path.join(pipeline_repo_path,"jobs/springmavenjob.yaml")
            yamlcontent=CommonFunctions.readyaml(yamlpath)
            logging.info("Selecting the Spring Pipeline Script using Maven")
            pipelinescript=SelectPipelineScript.selectpipeline(input)  
            pipelinefile=os.path.join(pipeline_repo_path,"pipeline/",pipelinescript)     
            if os.path.exists(pipelinefile) and os.path.getsize(pipelinefile) > 0:     
                modifiedyaml=SpringApplication.modifyyamlforspringmaven(yamlcontent,input,apprepo,pipelinescript)
                logging.info("Modifying the Spring Maven Yaml file based on the Developer inputs")
                if(CommonFunctions.writeyaml(modifiedyaml,'./springmavenjob.yaml')):
                    os.system('jenkins-jobs --conf ./jenkins_jobs.ini update ./springmavenjob.yaml')
                    logging.info('Spring job is created using Maven')
                    return ('Spring job is created using Maven')
                else:
                    return ('Error in writing Spring Maven yaml file')
            #else:
            #   return ('Spring Maven Pipelinescript is empty')
        except Exception as e:
            logging.info(e)

    def modifyyamlforspringgradle(yamlcontent,input,apprepo,pipelinescript):
        logging.info("Assigning the input values to Spring job placeholders using Gradle")
        for elem in yamlcontent:
            elem['job']['name']=input['ApplicationName']
            elem['job']['parameters'][0]['string']['default']=input['BuildName']
            elem['job']['parameters'][1]['string']['default']=apprepo
            elem['job']['parameters'][2]['string']['default']=config['credentials_id']
            elem['job']['parameters'][3]['string']['default']=input['ApplicationName']
            elem['job']['pipeline-scm']['scm'][0]['git']['url']=config['job_git_url']
            elem['job']['pipeline-scm']['scm'][0]['git']['credentials-id']=config['credentials_id']
            elem['job']['pipeline-scm']['script-path']='pipeline/'+ pipelinescript
            elem['job']['builders'][0]['gradle']['root-build-script-dir']=apprepo
            elem['job']['builders'][0]['gradle']['build-file']=input['File_Name']
            #elem['job']['builders'][1]['copyartifact']['project']=input['ApplicationName']
            #elem['job']['publishers'][0]['archive']['artifacts']=input['build_artifact_path']
            break
        return yamlcontent

    
    def modifyyamlforspringmaven(yamlcontent,input,apprepo,pipelinescript):
        logging.info("Assigning the input values to Spring job placeholders using Maven")
        for elem in yamlcontent:
            elem['job']['name']=input['ApplicationName']
            elem['job']['parameters'][0]['string']['default']=input['BuildName']
            elem['job']['parameters'][1]['string']['default']=apprepo
            elem['job']['parameters'][2]['string']['default']=config['credentials_id']
            elem['job']['parameters'][3]['string']['default']=input['ApplicationName']
            elem['job']['pipeline-scm']['scm'][0]['git']['url']=config['job_git_url']
            elem['job']['pipeline-scm']['scm'][0]['git']['credentials-id']=config['credentials_id']
            elem['job']['pipeline-scm']['script-path']='pipeline/'+ pipelinescript
            elem['job']['builders'][0]['maven-target']['maven-version']=input['Maven_Version']
            elem['job']['builders'][0]['maven-target']['pom']=input['pom_path']
            #elem['job']['publishers'][0]['archive']['artifacts']=input['build_artifact_path']
            break
        return yamlcontent

    
