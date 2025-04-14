# pipeline/annotation.py
import os
from utils.logging_utils import get_logger
from utils.file_utils import create_directory, execute_command

logger = get_logger()

def functional_annotation(binning_dir, output_dir, threads):
    """Perform functional annotation of bins."""
    annotation_dir = os.path.join(output_dir, "annotation")
    create_directory(annotation_dir)
    
    # Get all bin files
    bin_files = [os.path.join(binning_dir, f) for f in os.listdir(binning_dir) if f.endswith(".fa")]
    
    for bin_file in bin_files:
        bin_name = os.path.basename(bin_file).replace(".fa", "")
        bin_output_dir = os.path.join(annotation_dir, bin_name)
        create_directory(bin_output_dir)
        
        # Predict genes using Prodigal
        genes_file = os.path.join(bin_output_dir, f"{bin_name}_genes.faa")
        cmd = f"prodigal -i {bin_file} -a {genes_file} -p meta"
        execute_command(cmd, f"Predicting genes for {bin_name}")
        
        # Annotate with DIAMOND against KEGG
        kegg_results = os.path.join(bin_output_dir, f"{bin_name}_kegg.tsv")
        cmd = f"diamond blastp --db /path/to/kegg/db --query {genes_file} \
            --out {kegg_results} --outfmt 6 --evalue 1e-5 \
            --max-target-seqs 1 --threads {threads}"
        execute_command(cmd, f"KEGG annotation for {bin_name}")
        
        # Annotate with DIAMOND against CAZy
        cazy_results = os.path.join(bin_output_dir, f"{bin_name}_cazy.tsv")
        cmd = f"diamond blastp --db /path/to/cazy/db --query {genes_file} \
            --out {cazy_results} --outfmt 6 --evalue 1e-5 \
            --max-target-seqs 1 --threads {threads}"
        execute_command(cmd, f"CAZy annotation for {bin_name}")
    
    logger.info(f"Functional annotation completed. Results in {annotation_dir}")
    return annotation_dir
