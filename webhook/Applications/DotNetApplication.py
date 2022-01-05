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

class DotNetApplication:

    def createdotnetjob(input,apprepo):
        pipeline_repo_path=os.path.join(path,config['repo_name'])
        if os.path.isdir(pipeline_repo_path):
            logging.info("Pulling the Main repository")
            try:   
                CommonFunctions.gitpull(pipeline_repo_path)
                yamlpath=os.path.join(pipeline_repo_path,"jobs/dotnetjob.yaml")
                yamlcontent=CommonFunctions.readyaml(yamlpath)
                logging.info("Selecting the DotNet Pipeline Script")
                pipelinescript=SelectPipelineScript.selectpipeline(input)
                pipelinefile=os.path.join(pipeline_repo_path,"pipeline/",pipelinescript)     
                if os.path.exists(pipelinefile) and os.path.getsize(pipelinefile) > 0:     
                    modifiedyaml=DotNetApplication.modifyyamlfordotnet(yamlcontent,input,apprepo,pipelinescript)
                    logging.info("Modifying the DotNet Yaml file based on the Developer inputs")
                    if(CommonFunctions.writeyaml(modifiedyaml,'./dotnetjob.yaml')):
                        os.system('jenkins-jobs --conf ./jenkins_jobs.ini update ./dotnetjob.yaml')
                        logging.info('Dotnet job is created')
                        return ('Dotnet job is created')
                    else:
                        return ('Error in writing the DotNet yaml file')
                                    
                #else:
                #    return ('DotNet Pipeline Script is empty')
            except Exception as e:
                logging.info(e)
        else:
            logging.info("Cloning the Main Repository")
            try:    
                CommonFunctions.gitclone(path,config['job_git_url'])
                yamlpath=os.path.join(pipeline_repo_path,"jobs/dotnetjob.yaml")
                yamlcontent=CommonFunctions.readyaml(yamlpath)
                logging.info("Selecting the DotNet Pipeline Script")
                pipelinescript=SelectPipelineScript.selectpipeline(input)
                pipelinefile=os.path.join(pipeline_repo_path,"pipeline/",pipelinescript)     
                if os.path.exists(pipelinefile) and os.path.getsize(pipelinefile) > 0:     
                    modifiedyaml=DotNetApplication.modifyyamlfordotnet(yamlcontent,input,apprepo,pipelinescript)
                    logging.info("Modifying the DotNet Yaml file based on the Developer inputs")
                    if(CommonFunctions.writeyaml(modifiedyaml,'./dotnetjob.yaml')):
                        os.system('jenkins-jobs --conf ./jenkins_jobs.ini update ./dotnetjob.yaml')
                        logging.info('Dotnet job is created')
                        return ('Dotnet job is created')
                    else:
                        return ('Error in writing the DotNet yaml file')
                                    
                #else:
                #    return ('DotNet Pipeline Script is empty')
            except Exception as e:
                logging.info(e)


    def modifyyamlfordotnet(yamlcontent,input,apprepo,pipelinescript):
        logging.info("Assigning the input values to DotNet job placeholders")
        for elem in yamlcontent:
            elem['job']['name']=input['ApplicationName']
            elem['job']['parameters'][0]['string']['default']=input['BuildName']
            elem['job']['parameters'][1]['string']['default']=apprepo
            elem['job']['parameters'][2]['string']['default']=config['credentials_id']
            elem['job']['parameters'][3]['string']['default']=input['FileName']   # Input the application file name
            elem['job']['parameters'][4]['string']['default']=input['Branch']     # The branch where the developer code is committed
            elem['job']['pipeline-scm']['scm'][0]['git']['url']=config['job_git_url']
            elem['job']['pipeline-scm']['scm'][0]['git']['credentials-id']=config['credentials_id']
            elem['job']['pipeline-scm']['script-path']='pipeline/'+ pipelinescript
            elem['job']['builders'][0]['msbuild']['solution-file']=input['FileName'] # The builder name that needs to be used
            break
        return yamlcontent

    