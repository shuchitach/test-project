from prefect import task, Flow, Client
from python_terraform import *
from config import settings
from prefect.storage import Local, Azure, S3, GitHub
from prefect.run_configs import LocalRun
#import boto3

client = Client(
    api_server = settings.prefect_server
)

azstorage = Azure("flows", blob_name="test_blob")
githubstorage = GitHub(repo = "shuchitach/test-project", path="flow/flow.py")
#                        access_token_secret = "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")
#s3storage = S3(bucket="prefectst123")

def temp_prefect_run(project_name, flow_name):
    @task
    def run_terraform():
        tf = Terraform(working_dir="C:\\Users\\stripathi\\OneDrive - CITIHUB INC\\Documents\\composr\\orchestratr-api\\app\\tempdelete")
        tf.init()
        tf.plan()
        tf.apply(skip_plan=True)

    #with Flow(flow_name, storage=Azure(
    #    container="flows",
    #    connection_string_secret="DefaultEndpointsProtocol=https;AccountName=prefectflow;AccountKey=3TRIcCZVUvOCwA+u51kR7iDlatX0PMgKJBO99WR3C4irDIGWAGgEM2zT7pks/r98/fYuR6wuho+l5blguIv+zA==;EndpointSuffix=core.windows.net",
    #    #stored_as_script=True
    #    blob_name="test"
    #), run_config=LocalRun(labels=['CH-US-STRI01'], env={})) as f:      
    #    run_terraform()

    with Flow(flow_name, run_config=LocalRun(labels=['CH-US-STRI01'])) as f:
        run_terraform()

    f.storage = githubstorage
    client.register(f, project_name)

    #f.storage = Local()

    #f.register(project_name=project_name)
    #storage=Azure(container="flows"),


    
