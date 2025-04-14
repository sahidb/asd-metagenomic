# Analysis parameters
DEFAULT_THREADS = 8
MIN_CONTIG_LENGTH = 1000
MAX_BIN_SIZE = 2000

# Database paths
KEGG_DB_PATH = "/path/to/kegg_db"
CAZY_DB_PATH = "/path/to/cazy_db"
GTDBTK_DB_PATH = "/path/to/gtdbtk_db"

# Trimmomatic parameters
TRIMMOMATIC_SETTINGS = "ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"

# File extensions
FASTQ_EXTENSIONS = (".fastq", ".fq")
BIN_EXTENSION = ".fa"
