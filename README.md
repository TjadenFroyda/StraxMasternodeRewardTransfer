
Stratis/Cirrus Masternode Fee Consolidation and Mainchain Transfer
=======================================================
---
Author: TjadenFroyda

STRAX: XZSwKL8xB3CbKB4Sua5yqNzNm9PeKG1xJN

version: 1.0

---
Module for consolidating CIRRUS masternode reward utxo and transferring to STRAX mainchain.

Tested and working, but use at your own risk!!!!!

```
usage: python masternode_consolidate_and_transfer.py
```

Required nonstandard modules (pip install <module>):

* requests 
* python-decouple
* more-itertools
* cryptography
* getpass
* pytest (for testing)
* pytest-mock (for testing)
 
Notes:

The following variables must be set in a file named .env in the same folder as this module. 
```
CONSOLIDATION_ADDR='<YOUR CONSOLIDATION ADDRESS HERE>'
MAINCHAIN_ADDR='<YOUR MAINCHAIN ADDRESS HERE>'
```
OR
    
Modify those two strings in `masternode_consolidation_and_transfer.py` as shown in the code below with the respective addresses.
```
MAINCHAIN_ADDR = Address(address=config('<YOUR MAINCHAIN ADDRESS HERE>'), network=Network.STRAX)
CONSOLIDATION_ADDR = Address(address=config('<YOUR CONSOLIDATION ADDRESS HERE>'), network=Network.CIRRUS)
```

Recommend setting SIMULATE_TRANSACTIONS in `masternode_consolidate_and_transfer.py` to True for testing.

You can verify your **crosschain transfer address** by decoding the hexencoded **opReturnData** string. 

## Changelog

- Version 1.0
  
  - Address validation by network
  - Payload validation
  - API response models
  - Money validation
  - Custom exceptions
  - Improved credential handling
  - Unit testing
  - README documentation

- Version 0.1 
  
  - [Initial script](http://pastebin.com/VUarbCcE)

  