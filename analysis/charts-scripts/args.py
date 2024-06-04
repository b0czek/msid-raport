import argparse

def parse_arguments(desc = "Plot a chart from a CSV file", add_arguments = None): 
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('filename', type=str, help='Path to the CSV file')
    
    if add_arguments:
        add_arguments(parser)
    return parser.parse_args()