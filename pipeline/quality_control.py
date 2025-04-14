import os
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import file_utils, logging_utils
from config import TRIMMOMATIC_SETTINGS, FASTQ_EXTENSIONS

logger = logging_utils.setup_logger()

def run_trimmomatic(input_dir: str, output_dir: str, threads: int) -> str:
    """Perform quality control using Trimmomatic"""
    qc_dir = os.path.join(output_dir, "qc_data")
    file_utils.create_dir(qc_dir)
    
    # Process paired-end files
    for f in os.listdir(input_dir):
        if f.endswith(FASTQ_EXTENSIONS):
            base = f.split('_1')[0].split('_2')[0]
            r1 = os.path.join(input_dir, f"{base}_1.fastq")
            r2 = os.path.join(input_dir, f"{base}_2.fastq")
            
            if os.path.exists(r1) and os.path.exists(r2):
                output_prefix = os.path.join(qc_dir, base)
                cmd = (
                    f"trimmomatic PE -threads {threads} {r1} {r2} "
                    f"{output_prefix}_1_paired.fastq {output_prefix}_1_unpaired.fastq "
                    f"{output_prefix}_2_paired.fastq {output_prefix}_2_unpaired.fastq "
                    f"{TRIMMOMATIC_SETTINGS}"
                )
                file_utils.execute_command(cmd, logger)
    
    return qc_dir
