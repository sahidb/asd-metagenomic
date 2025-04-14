#!/usr/bin/env python3
import argparse
import os
from utils import logging_utils
from pipeline import (
    data_acquisition,
    quality_control,
    assembly,
    binning,
    taxonomy,
    annotation,
    analysis,
    reporting
)

def main():
    parser = argparse.ArgumentParser(description="ASD Gut Microbiome Analysis Pipeline")
    parser.add_argument("--project", required=True, help="NCBI SRA project ID")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--threads", type=int, default=8, help="Number of threads")
    args = parser.parse_args()

    # Setup
    logger = logging_utils.setup_logger(os.path.join(args.output, "pipeline.log"))
    os.makedirs(args.output, exist_ok=True)

    try:
        # Pipeline execution
        raw_data = data_acquisition.download_sra_data(args.project, args.output, args.threads)
        qc_data = quality_control.run_trimmomatic(raw_data, args.output, args.threads)
        assembly = assembly.assemble_metagenome(qc_data, args.output, args.threads)
        bins = binning.perform_binning(assembly, args.output, args.threads)
        taxonomy_results = taxonomy.classify_taxonomy(bins, args.output, args.threads)
        annotation_results = annotation.annotate_genomes(bins, args.output, args.threads)
        analysis_results = analysis.compare_groups(taxonomy_results, annotation_results, args.output)
        reporting.generate_report(args.output, args.project)

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
