import logging
import json,os
import azure.functions as func
from . import topic_classify as classifier

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid Request", status_code = 400)
    else:
        container_name = req_body.get('container_name')
        num_topics = req_body.get('num_topics')
        urls = classifier.classify(container_name,num_topics)
        headers_dict={}
        headers_dict["content-type"] = "application/json"
        if container_name:
            return func.HttpResponse(json.dumps(urls),status_code=200,headers=headers_dict)
        else:
            return func.HttpResponse(
                "Please pass a container name",status_code=400)
