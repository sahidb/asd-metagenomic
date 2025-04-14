import os
import subprocess
from typing import List

def create_directory(path: str) -> None:
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        
def execute_command(cmd: str, logger) -> bool:
    """Execute shell command with error handling"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        logger.info(f"Command succeeded: {cmd}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd}")
        logger.error(f"Error message: {e.stderr}")
        return False
