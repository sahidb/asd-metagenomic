"""
Functions for metagenomic binning.
"""


import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logging_utils import get_logger
from utils.file_utils import create_directory, execute_command

logger = get_logger()

def run_binning(assembly_dir, qc_dir, output_dir, threads):
    """Perform metagenomic binning using MetaBAT2."""
    binning_dir = os.path.join(output_dir, "binning")
    create_directory(binning_dir)
    
    # Path to final contigs
    contigs_file = os.path.join(assembly_dir, "final.contigs.fa")
    
    # Map reads back to contigs
    mapping_dir = os.path.join(output_dir, "mapping")
    create_directory(mapping_dir)
    
    # Get all paired FASTQ files
    sample_files = {}
    
    for file in os.listdir(qc_dir):
        if file.endswith("_paired.fastq"):
            sample_name = file.split("_")[0]
            if sample_name not in sample_files:
                sample_files[sample_name] = []
            sample_files[sample_name].append(os.path.join(qc_dir, file))
    
    # Map each sample to the assembly
    bam_files = []
    
    for sample_name, files in sample_files.items():
        if len(files) == 2:
            # Sort to ensure _1 comes before _2
            files.sort()
            
            output_bam = os.path.join(mapping_dir, f"{sample_name}.bam")
            bam_files.append(output_bam)
            
            # Map with BWA
            cmd = f"bwa index {contigs_file}"
            execute_command(cmd, f"Indexing contigs for {sample_name}")
            
            cmd = f"bwa mem -t {threads} {contigs_file} {files[0]} {files[1]} | \
                samtools view -bS - | \
                samtools sort -o {output_bam} -"
            execute_command(cmd, f"Mapping {sample_name} to contigs")
            
            cmd = f"samtools index {output_bam}"
            execute_command(cmd, f"Indexing BAM file for {sample_name}")
    
    # Generate depth file for MetaBAT2
    depth_file = os.path.join(binning_dir, "depth.txt")
    cmd = f"jgi_summarize_bam_contig_depths --outputDepth {depth_file} {' '.join(bam_files)}"
    execute_command(cmd, "Calculating contig depths")
    
    # Run MetaBAT2
    cmd = f"metabat2 -i {contigs_file} -a {depth_file} -o {binning_dir}/bin -t {threads} -m 2000"
    execute_command(cmd, "Running MetaBAT2 binning")
    
    logger.info(f"Binning completed. Results in {binning_dir}")
    return binning_dir
