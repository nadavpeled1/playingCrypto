"""
In this ex we are going to discover the crypto wallets domain:
Ex:
write a program that gets as input a list of wallet addresses and a list of dates,
and outputs the balance of each wallet in each date in a form of a table
"""

# 1. get input from user: list of wallets, list of dates
# 2. get data from the web
# 3. process the data
# 4. output the data


from web3 import Web3
import requests, os
import csv


INFURA_KEY = "744cb43f4bd64c859605dd7682394b9e"
ETHERSCAN_KEY = "U8M1Z3MQU8NFMTGVR9S3V8HQ8VH1FC9RGA"

def get_input():
    """
    This function gets input from the user
    input: 2 lists: wallets addresses, dates
    :return: list of wallet addresses and list of dates
    """
    wallet_list = []
    date_list = []
    wallet = input("Enter wallet address, or \"done\": ")
    while wallet != "done":
        wallet_list.append(wallet)
        wallet = input("Enter wallet address, or \"done\": ")

    date = input("Enter date, or \"done\": ")
    while date != "done":
        date_list.append(date)
        date = input("Enter date, or \"done\": ")

    return wallet_list, date_list

def get_data(wallet_list, date_list, infura_key, etherscan_key):
    """
    This function gets data from the web
    :param wallet_list: list of wallet addresses
    :param date_list: list of dates
    :param infura_key: Infura API key
    :param etherscan_key: Etherscan API key
    :return: list of wallet addresses, dates, and balance for each wallet in each date
    """
    balance_list = []
    for wallet in wallet_list:
        for date in date_list:
            balance = 0
            # get data from the web
            w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{infura_key}"))
            response = requests.get(f"https://api.etherscan.io/api?module=account&action=balance&address={wallet}&tag=latest&apikey={etherscan_key}")
            if response.status_code == 200:
                balance = int(response.json()["result"]) / 10**18
            balance_list.append((wallet, date, balance))
    return balance_list

def write_to_csv(output_file, balance_list, date_list):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        header = ["Wallet Address"] + [f"Balance at {date}" for date in date_list]
        writer.writerow(header)
        
        # Write the data
        for balance in balance_list:
            writer.writerow([balance[0]] + balance[2:])


def main():
    wallet_list, date_list = get_input()
    balance_list = get_data(wallet_list, date_list, INFURA_KEY, ETHERSCAN_KEY)
    for balance in balance_list:
        print(f"Wallet Address: {balance[0]}, Date: {balance[1]}, Balance: {balance[2]}")

if __name__ == "__main__":
    main()