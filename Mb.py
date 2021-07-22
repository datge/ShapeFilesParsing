from mapbox import Uploader
import os
import requests
import logging
import boto3
import json
from botocore.exceptions import ClientError
from ProgressPercentage import ProgressPercentage
from dotenv import load_dotenv

load_dotenv()


class Mb:
    def __init__(self):
        self.s3_resource = boto3.resource('s3')
        self.MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN')
        self.getAWSS3Keys()

    def getAWSS3Keys(self):
        response = requests.post(f"https://api.mapbox.com/uploads/v1/{os.getenv('MAPBOX_USERNAME')}/"
                                 f"credentials?access_token={os.getenv('MAPBOX_ACCESS_TOKEN')}").json()
        print(response)
        self.bucket = response['bucket']
        self.key = response['key']
        self.accessKeyId = response['accessKeyId']
        self.secretAccessKey = response['secretAccessKey']
        self.sessionToken = response['sessionToken']
        self.url = response['url']
        print(self.bucket)
        print("akey ", self.accessKeyId)
        print("skey ", self.secretAccessKey)
        print("sskey ", self.sessionToken)
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=self.accessKeyId,
            aws_secret_access_key=self.secretAccessKey,
            aws_session_token=self.sessionToken,
        )

    def createEmptyDataset(self):
        response = requests.post(
            f"https://api.mapbox.com/datasets/v1/datge93?access_token={os.getenv('MAPBOX_ACCESS_TOKEN')}",
            {"name": "foo", "description": "bar"}).json()
        print(response)

    def addFeatures(self, dataSetId: str, namePath):
        with open(f'GEOJson/{namePath}.json') as j:
            for index, feature in enumerate(json.load(j)['features']):
                feature['id'] = feature['properties']['ID']
                print(feature)
                print(dataSetId)
                print(feature['properties']['ID'])
                response = requests.put(
                    f"https://api.mapbox.com/datasets/v1/datge93/{dataSetId}/features/{feature['properties']['ID']}"
                    f"?access_token={os.getenv('MAPBOX_ACCESS_TOKEN')}",
                    headers={'content-type': 'application/json'},
                    data=json.dumps(feature)).json()
                print(response)
                #break

        '''
        response = requests.post(
            f"https://api.mapbox.com/datasets/v1/datge93/{dataSetId}/features/{feature_id}?access_token={os.getenv('MAPBOX_ACCESS_TOKEN')}",
            {"name": "foo", "description": "bar"}).json()
        print(response)        
        '''

    def uploadDataset(self, namePath: str, object_name=None):
        if object_name is None:
            object_name = namePath

        # Upload the file
        try:
            response = self.s3.upload_file(f'GEOJson/{namePath}.json', self.bucket, object_name)
            print(response)
        except ClientError as e:
            logging.error(e)
            return False
        return True

        # with open(f'GEOJson/{namePath}.json') as f:
        #    self.s3.upload_fileobj(f, self.bucket, '')
