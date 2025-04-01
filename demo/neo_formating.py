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
    no_rewards = False
    reward_rate = 0

    while i < len(lines):
        # Skip empty lines
        if not lines[i].strip():
            i += 1
            continue
        
        # Read description
        description = lines[i].strip()
        if description == "Reward Cashed Out" or description == "Neo Perks Payment" \
            or description == "Payment Received - Thank you" or description == "Membership Fee":
            no_rewards = True
            date_str = lines[i+1].strip()
            amount = lines[i+2].strip()

            # Identify if it's an incoming or outgoing amount
            if amount.startswith('-$'):
                amount_out = float(amount.replace('-$', '').replace(',', ''))
                amount_in = 0
            else:
                amount_out = 0
                amount_in = float(amount.replace('$', '').replace(',', ''))
        else:
            if lines[i+2].strip() == "Pending":
                i = i + 1
                break
            no_rewards = False
            date_str = lines[i+1].strip()
            if lines[i+2].strip().startswith('-$'):
                amount_out = float(lines[i+2].strip().replace('-$', '').replace(',', ''))
                amount_in = float(lines[i+3].strip().replace('$', '').replace(',', ''))
            else:
                # The transaction is a refund
                amount_out = 0
                amount_in = float(lines[i+2].strip().replace('$', '').replace(',', ''))
                no_rewards = True

        # Reformat the date to "2025-03-03"
        date = datetime.strptime(date_str, "%b %d").replace(year=2025).strftime("%Y-%m-%d")

        # # Check if it's pending
        # if 'Pending' in date:
        #     description += ' (Pending)'
        #     date = lines[i].strip()
        #     i += 1

        if not no_rewards:
            try:
                reward_rate = 100 * (float(amount_in) / float(amount_out))
                reward_rate = round(reward_rate, 2)
            except ZeroDivisionError:
                reward_rate = 0
            i += 4
        else:
            i += 3

        new_line = [date, description, amount_out, amount_in, f"Neo-4811 {description} - {reward_rate}%", reward_rate]
        print(new_line)
        transactions.append(new_line)
    
    df = pd.DataFrame(transactions, columns=[
        "Transaction Date", "Transaction Description", "Amount Out", "Amount In", "Neo Transaction Description", "Reward Rate"
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
