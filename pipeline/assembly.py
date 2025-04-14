import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import file_utils, logging_utils
from config import MIN_CONTIG_LENGTH


logger = logging_utils.setup_logger()

def assemble_metagenome(input_dir: str, output_dir: str, threads: int) -> str:
    """Perform metagenomic assembly using MEGAHIT"""
    assembly_dir = os.path.join(output_dir, "assembly")
    file_utils.create_dir(assembly_dir)
    
    cmd = (
        f"megahit -1 {input_dir}/*_1_paired.fastq -2 {input_dir}/*_2_paired.fastq "
        f"-o {assembly_dir} --min-contig-len {MIN_CONTIG_LENGTH} "
        f"-t {threads} --presets meta-sensitive"
    )
    file_utils.execute_command(cmd, logger)
    
    return assembly_dir
