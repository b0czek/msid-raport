import argparse
import pandas as pd
import numpy as np
def parse_arguments():
    parser = argparse.ArgumentParser(description="Filter a CSV file and save the results.")
    parser.add_argument('input_csv', type=str, help="Path to the input CSV file.")
    parser.add_argument('output_csv', type=str, help="Path to save the output CSV file.")

    return parser.parse_args()

def main():
    args = parse_arguments()

    df = pd.read_csv(args.input_csv)

    df = df[
        (df['furniture'] == True) &
        (df['price'] >= 1000) & (df['price'] < 10000) &
        (df['m'] >= 5) & (df['m'] < 125) &
        (df['latitude'] >= 51.04) & (df['latitude'] <= 51.19) &
        (df['longitude'] >= 16.83) & (df['longitude'] <= 17.19) 

    ]

    df['builttype'] = df['builttype'].replace(['szeregowiec', 'loft', 'wolnostojacy'], 'pozostale')

    df.to_csv(args.output_csv, index=False)
    print(f"Filtered data saved to {args.output_csv}")

if __name__ == "__main__":
    
    main()