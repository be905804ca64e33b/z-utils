"""
code modified from source:
https://www.quicknode.com/guides/web3-sdks/how-to-fetch-transaction-history-on-ethereum-using-web3-pys
ABI signature auto discovery
https://www.4byte.directory
"""
import os
import rich
import pandas as pd
from web3 import Web3, HTTPProvider
from dotenv import load_dotenv

load_dotenv('.env.public')

w3 = Web3(HTTPProvider(os.getenv('HTTP_PROVIDER')))

def get_txs(start: int, end: int, from_addr: str, to_addr: str) -> list:
    """
    Scans blocknumber start to end and returns a list of transactions that match the given from_addr, to_addr
    :param start: int block number
    :param end: int block number
    :param from_addr: str address
    :param to_addr: str address
    :return: list of txs
    """
    ret = []
    for i in range(start, end):
        print(f'Getting block {i}')
        block = w3.eth.getBlock(i, True)
        for transaction in block.transactions:
            if transaction['from'] == from_addr or transaction['to'] == to_addr:
                key = transaction['hash'].hex()
                ret.append({
                    'hash': key,
                    'raw_tx': transaction,
                })
    print(f"Finished searching blocks {start} through {end} and found {len(ret)} transactions")

    return ret

def txs_to_df(txs: list) -> pd.DataFrame:
    """
    Converts a list of transactions generated from get_txs() to a dataframe
    """
    df = pd.DataFrame(txs)
    df['from'] = df['raw_tx'].apply(lambda x: x['from'])
    df['to'] = df['raw_tx'].apply(lambda x: x['to'])
    
    return df

def main():
    ending_blocknumber = w3.eth.blockNumber
    starting_blocknumber = ending_blocknumber - 100  # look from the last x blocks
    addr = os.getenv('TARGET_ADDR')
    txs = get_txs(
        starting_blocknumber,
        ending_blocknumber,
        from_addr=addr,
        to_addr=addr
        )
    if len(txs) == 0:
        print('No transactions found in specified range')
        return
    df = txs_to_df(txs)
    rich.print(df)
    df.to_csv(os.path.join('output', 'txs.csv'))  # save to csv

if __name__ == "__main__":
    main()
