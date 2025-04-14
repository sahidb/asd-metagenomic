import pandas as pd
from typing import List
# from ..utils import file_utils, logging_utils
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Then use absolute imports
from utils import file_utils, logging_utils

logger = logging_utils.setup_logger()

def fetch_sra_accessions(project_id: str, output_dir: str) -> List[str]:
    """Retrieve SRA accessions for a given project"""
    runinfo_file = os.path.join(output_dir, "runinfo.csv")
    cmd = f"esearch -db sra -query {project_id} | efetch -format runinfo > {runinfo_file}"
    if not file_utils.execute_command(cmd, logger):
        raise RuntimeError("Failed to fetch SRA run information")
    
    return pd.read_csv(runinfo_file)['Run'].tolist()

def download_sra_data(project_id: str, output_dir: str, threads: int) -> str:
    """Download and convert SRA data"""
    download_dir = os.path.join(output_dir, "raw_data")
    file_utils.create_directory(download_dir)
    
    accessions = fetch_sra_accessions(project_id, output_dir)
    logger.info(f"Found {len(accessions)} SRA accessions")
    
    for sra_id in accessions:
        logger.info(f"Processing {sra_id}")
        # Download
        cmd = f"prefetch {sra_id} --output-directory {download_dir}"
        file_utils.execute_command(cmd, logger)
        
        # Convert to FASTQ
        cmd = f"fasterq-dump {download_dir}/{sra_id}/*.sra -O {download_dir} --split-files -e {threads}"
        file_utils.execute_command(cmd, logger)
    
    return download_dir
