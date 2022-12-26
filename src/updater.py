import logging
from os import path, system
from urllib import request
import zipfile
import requests
from packaging.version import parse
from datetime import datetime

# logger config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fmt = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

# streamHandler config
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(fmt)
streamHandler.setLevel(logging.DEBUG)
logger.addHandler(streamHandler)


def CheckNewVersion(version: str, gitHubRepo: str, TOKEN: str = None):
    """Gets the latest published release version of a GitHub repo and compares it to the given version
    
    # Arguments
        version: The current version of your software in string format
        gitHubRepo: The link to your GitHub repository in String format Example: https://github.com/jasger9000/Cryptographer
        TOKEN: If your repo is private you have to include an api token as a string

    # Returns
        String of version: If newer version was found
        False: Software version is newer or the same an latest version
        None: If repo was not found or no connection to GitHub was possible
    """
    if gitHubRepo[-1] != '/':
        gitHubRepo += '/'
        
    logger.info(f'Current version: {version}')
    try:
        logger.info('Trying to get latest version')
        if TOKEN:
            latest = requests.get(f'https://api.github.com/repos{gitHubRepo.split("github.com")[1]}releases/latest', headers={'Authorization': 'token ' + TOKEN}).json()['tag_name']
        else:
            latest = requests.get(f'https://api.github.com/repos{gitHubRepo.split("github.com")[1]}releases/latest').json()['tag_name']
        logger.info('Got latest version')
        logger.info(f'latest version: {latest}')
        if parse(latest) > parse(version):
            logger.info('Newer Version found')
            return latest
        else:
            logger.info('No new version found')
            return False
    except requests.ConnectionError:
        logger.info("Couldn't connect to server")
        return None
    except KeyError:
        logger.warning("The repo you are trying to reach does not exist or the application does not have the authorisation to access it")
        return None
    except IndexError:
        logger.error("The website url provided is not a GitHub url")
        return None

def DownloadVersion(version: str, gitHubRepo: str, downloadFile: str, applicationDir: str, delFiles: list[str] = None):
    """Downloads a version of an application from a GitHub repo
    
    # Arguments
    version: the version that is to be installed
    githubRepo: the link to the repository Expample: https://github.com/jasger9000/Cryptographer/
    downloadFile: The name of the file that is to be downloaded Exmaple: xyz.zip
    applicationDir: The director that the new version is to be installed in
    delFiles: Files and Dirs that should be deleted BEFORE installing the new update leave empty if none

    # Returns
    True: If package was downloaded correctly
    False: If something went wrong
    """
    
    # Adds a '/' to the end of the url if there was none so that the request still works
    if gitHubRepo[-1] != '/':
        gitHubRepo += '/'

    try:
        # Deletes Files and Directories that were provided in method call
        if delFiles: 
            logger.info(f'Deleting files and dirs from provided List')
            for file in delFiles:
                if path.isfile(file):
                    system(f"del /F /S /Q {applicationDir.replace('/', chr(92))}{chr(92)}{file}")
                    logger.info('Deleted file')
                elif path.isdir(file):
                    system(f"rmdir /S /Q {applicationDir.replace('/', chr(92))}{chr(92)}{file}")
                    logger.info('Deleted dir')
            logger.info(f'Every file/dir from list deleted')

        # Downloads the release from GitHub repo and saved it to the application directory provided in the method call
        url = f'{gitHubRepo}releases/download/{version}/{downloadFile}'
        file = f'{applicationDir}/{downloadFile}'
        logger.info(f'Downloading Update from {url}')
        request.urlretrieve(url, file)
        logger.info(f'Downloaded file and saved it to the application directory')

        return True
    except Exception:
        return False

def InstallVersion(applicationDir: str, versionFile: str, application: str, isZipFile: bool = False):
    """Installs a downloaded version and starts it"""
    system(f"del /F /S /Q {applicationDir}{chr(92)}{application}")
    
    if isZipFile:
        with zipfile.ZipFile(f'{applicationDir}{chr(92)}{versionFile}', 'r') as zip_ref:
            zip_ref.extractall(applicationDir)
        logger.info(f'Extracted files from {versionFile}')

    system(f"start {applicationDir}{chr(92)}{application}")
    return

def addFileHandlerLogging(logDir: str):
    """Adds a file handler for logging to this library"""

    fileHandler = logging.FileHandler(logDir)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(fmt)
    logger.addHandler(fileHandler)
