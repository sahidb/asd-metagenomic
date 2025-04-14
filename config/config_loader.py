"""
Configuration loader for ASD gut microbiome metagenomic analysis pipeline.
"""
import os
import yaml

class Config:
    """Configuration class for pipeline settings."""
    
    def __init__(self, config_file=None):
        """Initialize configuration from YAML file."""
        if config_file is None:
            # Default to config.yaml in the same directory as this file
            config_file = os.path.join(os.path.dirname(__file__), "config.yaml")
        
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def get_database(self, db_name):
        """Get database path."""
        return self.config["databases"].get(db_name)
    
    def get_file_param(self, param_name):
        """Get file parameter."""
        return self.config["files"].get(param_name)
    
    def get_tool_params(self, tool_name):
        """Get parameters for a specific tool."""
        return self.config.get(tool_name, {})
