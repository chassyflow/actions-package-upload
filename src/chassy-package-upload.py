#!/usr/bin/env python3

import argparse
import os
import pathlib
import sys
import glob
import logging
import requests

root_dir = "/github/workspace"
api_base_url = "https://api.test.chassy.dev/v1"

chassy_token = "eyJraWQiOiJ6a2QrV3FsNUg5S2J0dG1UYUJMcEdISUFuVDBEaDBNc3ByQ1wvU3NxRm9hWT0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiYlc5dmZjZW42YmhxSTRWaDZUN210QSIsInN1YiI6IjAyODZlMTczLWM3ZDMtNGE0Ny04ODc2LTA0MGY3OWZhNjI0ZCIsImNvZ25pdG86Z3JvdXBzIjpbInVzLXdlc3QtMl9hVGowbFpVdnJfR29vZ2xlIl0sImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtd2VzdC0yLmFtYXpvbmF3cy5jb21cL3VzLXdlc3QtMl9hVGowbFpVdnIiLCJjb2duaXRvOnVzZXJuYW1lIjoiR29vZ2xlXzExMzMwNzA1NTc3NDE4NDk1NDk5OCIsImdpdmVuX25hbWUiOiJTb21payIsIm5vbmNlIjoicnFuMk5ORTJpRmMyMlFjX0h3M2tmQzRXRTRIN1FMMHQtOTMyNWd6YTd2bmxsSUlTRUk3aE9PQjQzd09NaFVFNGRCR3JNRlRuZHRKTHpDSzRBZVBTNkFyOUVzRmdFZFAzbF8wdkhIZnk1TVRpZE1UU1ZSSmZvQWpCajVndkJjaG9WMVhSYVJjRGkteVhuMUt5OHlobDltU3FpdEVNUkNLU3k3cFJxT1NZbjljIiwicGljdHVyZSI6Imh0dHBzOlwvXC9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tXC9hXC9BQ2c4b2NLTzJrMy0zTVI0M0N4dk9LaTJYRTdZUllJSFJZYmt4TWE5WF9yYk1OOTBCNDdXNXc9czk2LWMiLCJvcmlnaW5fanRpIjoiYmJjOWRjZGEtOThkZS00YTQ1LTg5ODItNTJhODMyMDMzZjZjIiwiYXVkIjoiM2Y4anFtZWdrZzgycW5pc3JhZnFvN3JpM2oiLCJpZGVudGl0aWVzIjpbeyJ1c2VySWQiOiIxMTMzMDcwNTU3NzQxODQ5NTQ5OTgiLCJwcm92aWRlck5hbWUiOiJHb29nbGUiLCJwcm92aWRlclR5cGUiOiJHb29nbGUiLCJpc3N1ZXIiOm51bGwsInByaW1hcnkiOiJ0cnVlIiwiZGF0ZUNyZWF0ZWQiOiIxNzIzNDgxNTA4NzY2In1dLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTcyODgzOTA2OCwiZXhwIjoxNzI4ODgyMjY4LCJpYXQiOjE3Mjg4MzkwNjgsImZhbWlseV9uYW1lIjoiR2hvc2giLCJqdGkiOiI1MjQ1OThkZS04NTgwLTQwNTYtYmNkOC1mMDJmYTkxNWQ1ZDAiLCJlbWFpbCI6InNvbWlrQGNoYXNzeS5pbyJ9.fTbOnnSDyv05_ron_7U1ShZZB84mQWn-JW7O1xtsMU2qeJEijGPsxRiNfh8TJiArzc6NGx7YkM4a7TsAg73Q3VvuP4SAzF3KUIcSH20tDvLky3dWt5MJdXLfkuoPGnTmB7KacmIOQI4-fH94lqVe6xk4U1vkXiYAe8B4RB4MN_dbJezkdL5m7tLlJCQkCr7NMJfLuPhqLjV7lY0d9Qu8VEwG_oA7mVwdQ21XyQTjRaW-_TZgqkV80JQuxqhZr3ApDDvuO8OtiaOinJVoU2gFw77AZBNeT1MZUgsACajQOIpfM2EuK5PeRHSIQEqMdZoaPxx0RhHzkqc96B3yT8IhPg"
chassy_endpoint_dev = "https://api.test.chassy.dev"

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

class Args:
    def __init__(self):
        self.architecture = "ARM64"
        self.upload_type = "FILE"
        self.path = "/github/workspace/src/firmware/blinker.c"
        self.mode = "DEBUG"
        self.os_name = "ubuntu"
        self.os_version = "22.04"


# Function to easily write to github output.
def _write_to_github_output(key, value):
    """
    This function takes key and value to output to github actions workflow.
    
    Args:
        key (str): The key of the output. This must match the string in output section of actions.yml
        value (str): The value to assign to the string
    """    
    logger.error(f"Successfully wrote {key}={value} to $GITHUB_OUTPUT")
    return
    # # Get the path of the $GITHUB_OUTPUT environment variable
    # github_output = os.getenv('GITHUB_OUTPUT')
    
    # if github_output:
    #     # Open the file in append mode and write the key=value pair
    #     with open(github_output, 'a') as output_file:
    #         output_file.write(f"{key}={value}\n")
    #     logger.debug(f"Successfully wrote {key}={value} to $GITHUB_OUTPUT")
    # else:
    #     logger.debug("Error: $GITHUB_OUTPUT is not set in the environment")


def _check_preconditions(required_vars=None):
    """
    Ensures our expectations are met prior to execution to avoid any surprises during execution.
    Primarily checks that specified required_vars are defined as environment variables.
    :return:
    """
    if required_vars is None:
        required_vars = []
    for value in required_vars:
        logger.error(f"env var {value} has value of {os.getenv(value)}")
        if os.getenv(value) is None:
            logger.error(f"critical variable {value} is missing.")
            raise Exception(f"could not find required value {value}.")


def _find_files(file_pattern):
    """
    This function takes a file name, a directory pattern, or a file prefix with wildcards.
    It searches for the file and returns the full file path.
    
    Args:
        file_pattern (str): The name of the file, or a pattern with wildcards, or the parent directory pattern.
        
    Returns:
        a generator for all files discovered matching pattern
    """
    
    # Use glob to search for the file pattern
    # The '**' pattern in glob searches recursively in subdirectories.
    files_found = glob.glob(os.path.join(root_dir, '**', file_pattern), recursive=True)

    for file in files_found:
        yield os.path.abspath(file)


def _get_credentials():
    # @ghoshsomik test code
    return chassy_token
    chassy_refresh_token_b64 = os.getenv('CHASSY_TOKEN')
    if chassy_refresh_token_b64 in (None, ''):
        raise KeyError("Environment variable 'CHASSY_TOKEN' not found.")
    
    logger.debug("making request to refresh token")

    refresh_token_url = f"{api_base_url}/token/user"
    token_request_body = {
        "token": chassy_refresh_token_b64
    }

    try:
        response = requests.post(
            refresh_token_url,
            headers={"Content-Type": "application/json"},
            json=token_request_body
        )
        # Raises HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        refresh_token_response = response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.critical(f"HTTP error occurred: {http_err}")  # HTTP error
    except Exception as err:
        logger.critical(f"An error occurred: {err}")  # Other errors

    return refresh_token_response.idToken


def _get_upload_url(credentials: str,
                    name: str,
                    architecture: str,
                    os_name: str,
                    os_version: str,
                    type: str):
    base_url, url = None, None
    # if os.getenv('CHASSY_ENDPOINT') is None:
    #     base_url = 'https://api.chassy.io'
    # else:
    #     base_url = os.getenv('CHASSY_ENDPOINT')
    base_url = chassy_endpoint_dev
    if type == 'IMAGE':
        url = f"{base_url}/image"
    else:
        url = f"{base_url}/package"

    json_payload = {
        'name': name,
        'compatibility': {
            'versionID': os_version,
            'osID': os_name,
            'architecture': architecture
        },
        'type': type,
        'provenanceURI': os.getenv('GITHUB_REF', 'N/A'),
    }

    # Log payload for debugging
    logger.debug("JSON Payload:")
    for key, value in json_payload.items():
        logger.debug(f"  {key}: {value} (type: {type(value)})")

    try:
        response = requests.post(url,
                                 json=json_payload,
                                 headers={
                                     'Authorization': credentials
                                 })
        response.raise_for_status()  # Raises HTTPError for bad responses
        response_data = response.json()
        logger.debug(f"Response JSON: {response_data}")
        return response_data.get('uploadURI')  # Adjust based on actual response structure
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        logger.debug(f"Response Content: {response.text}")
        return None


def _put_a_file(upload_url, file_path):
    """
    This function takes a destination URL and a fully qualified file path and uploads the file to the URL as a PUT request
    
    Args:
        upload_url (str): the URL to upload the file to.
        file_path (str): the fully qualified file path to upload to
    """
    with open(file_path, 'rb') as file:
        headers = {'Content-Type': 'application/octet-stream'}
        logger.debug(f"starting upload of file {file_path} to {upload_url}")
        response = requests.put(upload_url, data=file, headers=headers)

    # Check the response status
    if response.ok:
        logger.debug('File uploaded successfully.')
    else:
        logger.debug(f'Failed to upload file. Status code: {response.status_code}')
        logger.debug('Response:', response.text)
        # raise an http error since things aren't okay
        response.raise_for_status()

def _image_uploads(args):
    """
    Core routine responsible for uploading images to Chassy registry.
    :param args:
    :return:
    """
    for image_file in _find_files(str(args.path)):
        logger.debug(f"discovered {image_file} to be processed")
        _f = pathlib.Path(image_file)
        file_name = _f.name

        # remove any suffixes e.g .img from file to extract canonical name
        if _f.suffix:
            file_name = file_name.strip(_f.suffix)

        logger.debug(f"logical name of image is {file_name}")
        authorization_token = _get_credentials()

        upload_url = _get_upload_url(authorization_token, file_name, args.architecture, args.os_name, args.os_version, args.upload_type)
        _put_a_file(upload_url, args.path)
   
    return True


def _file_uploads(args):
    """
    Core routine responsible for uploading binaries/files/archives to Chassy registry
    :param args:
    :return:
    """
    for file in _find_files(str(args.path)):
        logger.debug(f"discovered {file} to be processed")
        _f = pathlib.Path(file)
        file_name = _f.name    

        # remove any suffixes e.g .img from file to extract canonical name
        if _f.suffix:
            file_name = file_name.strip(_f.suffix)

        logger.debug(f"logical name of image is {file_name}")
        authorization_token = _get_credentials()
        upload_url = _get_upload_url(authorization_token, file_name, args.architecture, args.os_name, args.os_version, args.upload_type)
        _put_a_file(upload_url, args.path)

    return True


def _handler(args) -> int:
    if args.mode == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # _check_preconditions("GITHUB_OUTPUT")
    # _check_preconditions("CHASSY_TOKEN")
    # _check_preconditions("CHASSY_ENDPOINT")        

    if args.upload_type == 'IMAGE':
        status = _image_uploads(args)
    else:
        status = _file_uploads(args)

    if status is True:
        _write_to_github_output("Status", "Successfully uploaded file.")

def main() -> int:
    """
    initiates execution of this application, chiefly responsible for parsing parameters.
    :return:
    """
    print("\n\nCommand-line arguments:", sys.argv)  # Print the raw arguments

    args = Args()
    return _handler(args)

    # parser = argparse.ArgumentParser(prog='chassy-package-upload',
    #                                  description='chassy artifact and image uploader')
    # parser.set_defaults(func=_handler)
    # parser.add_argument('-p',
    #                       '--path',
    #                       required=True,
    #                       action='store',
    #                       type=pathlib.Path,
    #                       help='fully qualified path to image file or a glob search path for image')
    # parser.add_argument('-a',
    #                       '--architecture',
    #                       choices=["AMD64", "ARM64", "ARMv6", "ARMv7", "RISCV", "UNKNOWN"],
    #                       required=True,
    #                       action='store',
    #                       help='architecture of image to be uploaded')
    # parser.add_argument('-o',
    #                     '--os',
    #                     action='store',
    #                     required=True,
    #                     help='operating system name for compatibility tracking')
    # parser.add_argument('-i',
    #                     '--version',
    #                     action='store',
    #                     required=True,
    #                     help='operating system version for compatibility tracking')
    # parser.add_argument('-t',
    #                     '--type',
    #                     action='store',
    #                     choices=["FILE", "ARCHIVE", "IMAGE", "FIRMWARE"],
    #                     required=True,
    #                     help='what is the artifact type')
    # parser.add_argument('-c',
    #                     '--classification',
    #                     action='store',
    #                     choices=["EXECUTABLE", "CONFIG", "DATA", "BUNDLE"],
    #                     required=False,
    #                     help='for file and archives, what is the class of artifact')
    # parser.add_argument('-m',
    #                     '--mode',
    #                     choices=['DEBUG', 'INFO'],
    #                     required=False,
    #                     default='INFO',
    #                     help='determine if we should run in debug or standard info mode')
    # parser.add_argument('-d',
    #                       '--dryrun',
    #                       action='store_true',
    #                       help='determine if we should run in dryrun mode or not',
    #                       required=False,
    #                       default=False)    
    # args = parser.parse_args()
    # return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
