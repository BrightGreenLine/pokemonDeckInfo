import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import json
import os, os.path
from dotenv import load_dotenv

load_dotenv()


def get_pkio_key():
    """Return the api key from the source. Temporarily, file on my drive"""
    if(os.getenv('HOST')=="LOCAL" or os.getenv('HOST')==""):
        with open(os.path.join(os.getenv('SECRETS_PATH'),"ptcgio_apikey.txt"), "rt", encoding='UTF-8') as file:
            result = file.read()
            return result
    elif (os.getenv('HOST')=="AWS"):
        response = get_aws_secret('pkio_api_key', os.getenv('AWSREGION'))
        result = json.loads(response['SecretString'])['pkio_key']
        return result



def get_cards_DSN():
    """Return the api key from the source. Temporarily, file on my drive"""
    if(os.getenv('HOST')=="LOCAL" or os.getenv('HOST')==""):
        with open(os.path.join(os.getenv('SECRETS_PATH'),"cardDB.txt"), "rt", encoding='UTF-8') as file:
            result = file.read()
            return result
    elif (os.getenv('HOST')=="AWS"):
        response = get_aws_secret('cardinfo_DSN', os.getenv('AWSREGION'))
        result = json.loads(response['SecretString'])['DSN']
        return result
    


def get_aws_secret(secret_name, region):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region)

    try:
        response = client.get_secret_value(SecretID=secret_name)
    except ClientError as error:
        match error.response['Error']['Code']:
            case 'ResourceNotFoundException':
                error_message = f"The requested secret {secret_name} was not found"
            case 'InvalidRequestException':
                error_message = f"The request was invalid due to: {error}"
            case 'InvalidParameterException':
                error_message = f"The request had invalid params: {error}"
            case 'DecryptionFailure':
                error_message = f"The requested secret can't be decrypted using the provided KMS key: {error}"
            case 'InternalServiceError':
                error_message = f"An error occurred on service side: {error}"
        print(f"{datetime.now()} | ERROR | {error_message}")
        results = None
    else:
        results = response
    return results