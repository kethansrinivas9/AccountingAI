import os
import string
import boto3


def get_parameter_value(parameter_name: str):
    ssm_client = boto3.client('ssm', region_name='us-east-1')
    try:
        response = ssm_client.get_parameter(
            Name=parameter_name,
            WithDecryption=True  # Decrypt if it's a secured parameter
        )
        return response['Parameter']['Value']
    except ssm_client.exceptions.ParameterNotFound:
        print(f"Parameter {parameter_name} not found")
        return None
    except Exception as e:
        print(f"Error fetching parameter: {str(e)}")
        return None

def load_envs_that_are_not_already_loaded(params: list[string]):
    for param in params:
        param_value = os.getenv(param)
        if not param_value:
            print(f"Environment variable not found for {param}. Fetching from SSM...")
            os.environ[param] = get_parameter_value(param)
            print(f"Parameter value loaded after setting for {param} is {os.getenv(param)}")
        else:
            print(f"Parameter value found in environment variables for {param} is {os.getenv(param)}")


def load_params_from_aws_ssm():
    # Specify the parameter name you want to retrieve
    parameter_names = ['OPENAI_API_KEY', 'DATABASE_URL']

    load_envs_that_are_not_already_loaded(parameter_names)
