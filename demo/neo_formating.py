import re
import pandas as pd
import sys
import os
from datetime import datetime

def parse_transaction_data(file_path, output_csv):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    transactions = []
    i = 0
    while i < len(lines):
        description = lines[i].strip()
        print(description)
        i += 1
        
        if i >= len(lines):
            break
        
        date_str = lines[i].strip()
        # Reformat the date to "2025-03-03"
        date = datetime.strptime(date_str, "%b %d").replace(year=2025).strftime("%Y-%m-%d")
        i += 1
        
        # # Check if it's pending
        # if 'Pending' in date:
        #     description += ' (Pending)'
        #     date = lines[i].strip()
        #     i += 1
        
        # Read amounts
        j = 0
        # while i < len(lines) and lines[i].strip() and j < 2:
        amount_str = lines[i].strip()
            
            # # Skip date lines
            # if re.match(r'^[A-Za-z]{3} \d{2}', amount_str):
            #     break
            
            # # Skip description lines
            # if not re.match(r'^-?\$?\d+(\.\d{2})?$', amount_str.replace(',', '')):
            #     i += 1
            #     continue
            
            # Identify if it's an incoming or outgoing amount
        if amount_str.startswith('-$'):
            amount_out = float(amount_str.replace('-$', '').replace(',', ''))
            amount_in = ''
        else:
            amount_in = float(amount_str.replace('$', '').replace(',', ''))
            amount_out = ''
            
        if description == "Reward Cashed Out" or description == "Neo Perks Payment" or description == "Payment Received - Thank you":
            i += 1
        else:
            i += 2
    
        transactions.append([date, description, amount_out, amount_in, f"Neo-4811-{description}"])
    
    df = pd.DataFrame(transactions, columns=[
        "Transaction Date", "Transaction Description", "Amount Out", "Amount In", "Neo Transaction Description"
    ])
    df.to_csv(output_csv, index=False)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file.txt>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    output_file = os.path.splitext(input_file)[0] + "-formatted.csv"
    parse_transaction_data(input_file, output_file)
    print(f"CSV file created: {output_file}")

if __name__ == "__main__":
    main()
