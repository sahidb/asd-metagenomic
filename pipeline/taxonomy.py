"""
Taxonomic Classification Module

This module performs taxonomic classification of metagenomic bins using GTDB-Tk.
"""

import os
from utils.logging_utils import get_logger
from utils.file_utils import create_directory, execute_command

logger = get_logger()

def taxonomic_classification(binning_dir, output_dir, threads):
    """
    Perform taxonomic classification of bins using GTDB-Tk.
    
    Args:
        binning_dir (str): Path to the directory containing metagenomic bins.
        output_dir (str): Path to the main output directory.
        threads (int): Number of threads to use.

    Returns:
        str: Path to the directory containing taxonomic classification results.
    """
    taxonomy_dir = os.path.join(output_dir, "taxonomy")
    create_directory(taxonomy_dir)
    
    # Run GTDB-Tk classify workflow
    cmd = f"gtdbtk classify_wf --genome_dir {binning_dir} --out_dir {taxonomy_dir} \
        --extension fa --cpus {threads}"
    execute_command(cmd, "Running GTDB-Tk for taxonomic classification")
    
    logger.info(f"Taxonomic classification completed. Results in {taxonomy_dir}")
    return taxonomy_dir
