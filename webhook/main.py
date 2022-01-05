import flask,json,logging
import os.path
from flask import request
from ruamel.yaml import YAML


from Applications.CommonFunctions import CommonFunctions
from Applications.Reactapplication import ReactApplication
from Applications.SpringApplication import SpringApplication
from Applications.AngularApplication import AngularApplication
from Applications.DotNetApplication import DotNetApplication

app = flask.Flask(__name__)
app.config["DEBUG"] = True
yaml=YAML()
with open('./config.json') as f:
    config=json.load(f)
    
path = config['default_home_path']

LOG_FILENAME = 'Info.log'
logging.basicConfig(filename=LOG_FILENAME, filemode='a', level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')  
logging.info('*****************Dynamic DevOps Pipeline Creation*****************')


@app.route('/', methods=['GET','POST'])
def home():
    logging.info('*****************Dynamic DevOps Pipeline Creation*****************') 
    try:
        data=request.json
        repo_path=os.path.join(path,request.json['repository']['name'])
    except Exception as e:
        logging.info(e)
    output = None
    logging.info("Checking if the Application Repository path is present or not")
    if os.path.isdir(repo_path):
        logging.info("Pulling the Application repository")
        CommonFunctions.gitpull(repo_path)
        output=CommonFunctions.inputfunc(repo_path)
    else:
        logging.info("Cloning the Application repository")
        CommonFunctions.gitclone(path,request.json['repository']['clone_url'])
        output=CommonFunctions.inputfunc(repo_path)
    
    if output['ApplicationType'] == 'React':
        apprepo=request.json['repository']['clone_url']
        logging.info("Calling the React Job creation function")
        final_output=ReactApplication.createreactjob(output,apprepo)
        return json.dumps(final_output)
    elif output['ApplicationType'] == 'Spring':
        apprepo=request.json['repository']['clone_url']
        logging.info("Calling the Spring Job creation function")
        final_output=SpringApplication.createspringjob(output,apprepo)
        return json.dumps(final_output)
    elif output['ApplicationType'] == 'Angular':
        apprepo=request.json['repository']['clone_url']
        logging.info("Calling the Angular Job creation function")
        final_output=AngularApplication.createangularjob(output,apprepo)
        return json.dumps(final_output)
    elif output['ApplicationType'] == 'Dotnet':
            apprepo=request.json['repository']['clone_url']
            logging.info("Calling the DotNet Job creation function")
            final_output=DotNetApplication.createdotnetjob(output,apprepo)
            return json.dumps(final_output)
    else:
        return ('Invalid Application Type')


app.run(host="0.0.0.0")
