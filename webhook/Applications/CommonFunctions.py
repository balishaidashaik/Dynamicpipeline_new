import flask,git,json,os.path,logging
from ruamel.yaml import YAML


app = flask.Flask(__name__)
app.config["DEBUG"] = True
yaml=YAML()
with open('./config.json') as f:
    config=json.load(f)
    
path = config['default_home_path']

class CommonFunctions: 

    def gitpull(path):
        repo=git.Repo(path) 
        repo.remotes.origin.pull()

    def gitclone(path,repo):
        git.Git(path).clone(repo)

    def readyaml(path):
        logging.info('Reading the Application Yaml File')
        fp=open(path).read()
        yamlcontent=yaml.load(fp)
        return yamlcontent

    def writeyaml(obj,str):
        logging.info('Writing into the Application Yaml File')
        fp=open(str,"w")
        yaml.dump(obj,fp)
        return True
    
    def inputfunc(str):
        logging.info('Taking input form the Developers Config File')
        with open(os.path.join(path,str)+'/pipeline_config.json') as f:
            input=json.load(f)
        return input
    