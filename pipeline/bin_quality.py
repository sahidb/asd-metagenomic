"""
Functions for assessing bin quality.
"""

import os
from utils.logging_utils import get_logger
from utils.file_utils import create_directory, run_command
from config import BIN_EXTENSION

logger = get_logger()

def assess_bin_quality(binning_dir, output_dir, threads):
    """Assess the quality of metagenomic bins using CheckM."""
    checkm_dir = os.path.join(output_dir, "checkm")
    create_directory(checkm_dir)
    
    # Run CheckM
    cmd = f"checkm lineage_wf -t {threads} -x {BIN_EXTENSION} {binning_dir} {checkm_dir}"
    run_command(cmd, "Running CheckM to assess bin quality")
    
    # Generate summary table
    cmd = f"checkm qa -o 2 -f {checkm_dir}/quality_summary.tsv --tab_table -t {threads} \
        {checkm_dir}/lineage.ms {checkm_dir}"
    run_command(cmd, "Generating CheckM quality summary")
    
    logger.info(f"Bin quality assessment completed. Results in {checkm_dir}")
    return checkm_dir
