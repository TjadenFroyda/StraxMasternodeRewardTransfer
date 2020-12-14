#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from decouple import config
from datetime import datetime, timedelta
from consolidate import consolidate
from transfer import transfer
from utilities import Credentials, Network, Address

MIN_CONF = 0
MAX_BUILD_ATTEMPTS = 10
BATCH_SIZE = 64
HOURS_BETWEEN_CONSOLIDATIONS = 6
SECONDS_PER_HOUR = 3600
WALLETNAME = 'MiningWallet'
CIRRUS_FEDERATION_ADDR = Address(address='cYTNBJDbgjRgcKARAvi2UCSsDdyHkjUqJ2', network=Network.CIRRUS)
MAINCHAIN_ADDR = Address(address=config('MAINCHAIN_ADDR'), network=Network.STRAX)
CONSOLIDATION_ADDR = Address(address=config('CONSOLIDATION_ADDR'), network=Network.CIRRUS)
SIMULATE_TRANSACTIONS = False


if __name__ == '__main__':
    creds = Credentials(wallet_name=WALLETNAME)
    creds.set_wallet_password()

    while True:
        try:
            # Transfer mature, consolidated utxos to mainchain first
            transfer(
                credentials=creds,
                consolidation_address=CONSOLIDATION_ADDR,
                federation_address=CIRRUS_FEDERATION_ADDR,
                mainchain_address=MAINCHAIN_ADDR,
                max_build_attempts=MAX_BUILD_ATTEMPTS,
                min_conf=MIN_CONF,
                simulate=SIMULATE_TRANSACTIONS)

            # Move other utxos to the consolidation address
            consolidate(
                credentials=creds,
                consolidation_address=CONSOLIDATION_ADDR,
                batch_size=BATCH_SIZE,
                simulate=SIMULATE_TRANSACTIONS)
        except Exception as e:
            # This will catch connection errors, such as when the cirrus node is not running.
            print(e)

        print(f'Done with consolidation at {datetime.now()}.\nNext run: {datetime.now() + timedelta(hours=HOURS_BETWEEN_CONSOLIDATIONS)}.')
        time.sleep(SECONDS_PER_HOUR * HOURS_BETWEEN_CONSOLIDATIONS)
