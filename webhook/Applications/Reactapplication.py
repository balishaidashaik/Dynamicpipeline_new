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
class ReactApplication:
    
    def modifyyamlforreact(yamlcontent,input,apprepo,pipelinescript):
        logging.info("Assigning  the input values to React job placeholders")
        for elem in yamlcontent:
            elem['job']['name']=input['ApplicationName']
            elem['job']['parameters'][0]['string']['default']=input['BuildName']
            elem['job']['parameters'][1]['string']['default']=apprepo
            elem['job']['parameters'][2]['string']['default']=config['credentials_id']
            elem['job']['parameters'][3]['string']['default']=input['ApplicationName']
            elem['job']['pipeline-scm']['scm'][0]['git']['url']=config['job_git_url']
            elem['job']['pipeline-scm']['scm'][0]['git']['credentials-id']=config['credentials_id']
            elem['job']['pipeline-scm']['script-path']='pipeline/'+ pipelinescript
            break
        return yamlcontent

    def createreactjob(input,apprepo):
        pipeline_repo_path=os.path.join(path,config['repo_name'])
        if os.path.isdir(pipeline_repo_path):
            logging.info("Pulling the Main repository")
            try:
                CommonFunctions.gitpull(pipeline_repo_path)
                yamlpath=os.path.join(pipeline_repo_path,"jobs/reactjob.yaml")
                yamlcontent=CommonFunctions.readyaml(yamlpath)
                logging.info("Selecting the React Pipeline Script")
                pipelinescript=SelectPipelineScript.selectpipeline(input)
                pipelinefile=os.path.join(pipeline_repo_path,"pipeline/",pipelinescript)     
                if os.path.exists(pipelinefile) and os.path.getsize(pipelinefile) > 0:     
                    modifiedyaml=ReactApplication.modifyyamlforreact(yamlcontent,input,apprepo,pipelinescript)
                    if(CommonFunctions.writeyaml(modifiedyaml,'./reactjob.yaml')):
                        os.system('jenkins-jobs --conf ./jenkins_jobs.ini update ./reactjob.yaml')
                        logging.info('React job is created')
                        return ('React job is created')
                    else:
                        return ('Error in writing the React yaml file')
                #else:
                #    return ('React Pipeline scipt is empty')
            except Exception as e:
                logging.info(e)
        else:
            logging.info("Cloning the Main repository")
            try:
                CommonFunctions.gitclone(path,config['job_git_url'])
                yamlpath=os.path.join(pipeline_repo_path,"jobs/reactjob.yaml")
                yamlcontent=CommonFunctions.readyaml(yamlpath)
                logging.info("Selecting the React Pipeline Script")
                pipelinescript=SelectPipelineScript.selectpipeline(input)
                pipelinefile=os.path.join(pipeline_repo_path,"pipeline/",pipelinescript)     
                if os.path.exists(pipelinefile) and os.path.getsize(pipelinefile) > 0:     
                    modifiedyaml=ReactApplication.modifyyamlforreact(yamlcontent,input,apprepo,pipelinescript)
                    if(CommonFunctions.writeyaml(modifiedyaml,'./reactjob.yaml')):
                        os.system('jenkins-jobs --conf ./jenkins_jobs.ini update ./reactjob.yaml')
                        logging.info('React job is created')
                        return ('React job is created')
                    else:
                        return ('Error in writing the React yaml file')
                #else:
                #    return ('React Pipeline scipt is empty')
            except Exception as e:
                logging.info(e)
    
    

