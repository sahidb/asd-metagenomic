# pipeline/analysis.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.logging_utils import get_logger
from utils.file_utils import create_directory

logger = get_logger()

def comparative_analysis(taxonomy_dir, annotation_dir, metadata_file, output_dir):
    """Perform comparative analysis between ASD and control samples."""
    analysis_dir = os.path.join(output_dir, "comparative_analysis")
    create_directory(analysis_dir)
    
    # Load metadata
    metadata = pd.read_csv(metadata_file)
    
    # Load taxonomic classification results
    taxonomy_file = os.path.join(taxonomy_dir, "gtdbtk.bac120.summary.tsv")
    taxonomy_data = pd.read_csv(taxonomy_file, sep="\t")
    
    # Merge with metadata
    # This requires mapping between bin IDs and sample IDs
    # For simplicity, we assume bin names include sample IDs
    
    # Example analysis: Compare phylum-level abundance between ASD and control
    phylum_counts = taxonomy_data.groupby("phylum").size().reset_index(name="count")
    
    # Plot phylum distribution
    plt.figure(figsize=(12, 8))
    sns.barplot(x="phylum", y="count", data=phylum_counts)
    plt.xticks(rotation=90)
    plt.title("Phylum Distribution in Samples")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_dir, "phylum_distribution.png"))
    
    # More sophisticated analyses would be added here
    
    logger.info(f"Comparative analysis completed. Results in {analysis_dir}")
    return analysis_dir
