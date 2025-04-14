# pipeline/reporting.py
import os
import time
from utils.logging_utils import get_logger
from utils.file_utils import create_directory

logger = get_logger()

def generate_report(output_dir, project_id):
    """Generate a comprehensive report of the analysis."""
    report_dir = os.path.join(output_dir, "report")
    create_directory(report_dir)
    
    # Create HTML report
    report_file = os.path.join(report_dir, "report.html")
    
    with open(report_file, "w") as f:
        f.write("<html>\n")
        f.write("<head>\n")
        f.write("<title>ASD Gut Microbiome Analysis Report</title>\n")
        f.write("<style>body { font-family: Arial; margin: 40px; }</style>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        
        f.write(f"<h1>ASD Gut Microbiome Analysis Report</h1>\n")
        f.write(f"<p>Project: {project_id}</p>\n")
        f.write(f"<p>Date: {time.strftime('%Y-%m-%d')}</p>\n")
        
        f.write("<h2>Analysis Summary</h2>\n")
        
        # Add sections for each analysis step
        
        f.write("<h2>Taxonomic Composition</h2>\n")
        f.write(f"<img src='../comparative_analysis/phylum_distribution.png' width='800'>\n")
        
        # Add more sections as needed
        
        f.write("</body>\n")
        f.write("</html>\n")
    
    logger.info(f"Report generation completed. Results in {report_dir}")
    return report_dir
