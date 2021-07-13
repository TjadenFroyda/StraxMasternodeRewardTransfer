
Stratis/Cirrus Masternode Mainchain Transfer Script
=======================================================
---
Author: TjadenFroyda

STRAX: XZSwKL8xB3CbKB4Sua5yqNzNm9PeKG1xJN

version: 2.0

---
Module for transfering CIRRUS masternode reward utxo to STRAX mainchain.

Tested and working, but use at your own risk!!!!!

#### Usage
```commandline
python masternode_transfer_to_mainchain.py
```

Required nonstandard modules (pip install <module>):

* pystratis 
* python-decouple
* cryptography
 
### Notes

The following variables must be set in a file named .env in the same folder as this module. 
```text
SENDING_ADDRESS='<YOUR SENDING ADDRESS HERE>'
MAINCHAIN_ADDRESS='<YOUR MAINCHAIN ADDRESS HERE>'
```
OR
    
Modify those two strings in `masternode_transfer_to_mainchain.py` as shown in the code below with the respective addresses.
```python
MAINCHAIN_ADDRESS = Address(address='<YOUR MAINCHAIN ADDRESS HERE>', network=StraxMain())
SENDING_ADDRESS = Address(address='<YOUR SENDING ADDRESS HERE>', network=CirrusMain())
```

Recommend setting SIMULATE_TRANSACTIONS in `masternode_transfer_to_mainchain.py` to True for testing.

You can verify your **crosschain transfer address** by decoding the hexencoded **OP_RETURN** string. 

This is done during transaction simulation and printed for inspection. 

### Changelog
#### Version 2.0
- [pystratis](http://github.com/stratisproject/pystratis) refactor.
- Most of the functionality from version 1.0 has been incorporated into pystratis. 

#### Version 1.0
- Address validation by network
- Payload validation
- API response models
- Money validation
- Custom exceptions
- Improved credential handling
- Unit testing
- README documentation

#### Version 0.1
- [Initial script](http://pastebin.com/VUarbCcE)

  