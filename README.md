
Stratis/Cirrus Masternode Reward Transfer Script
=======================================================
---
Author: TjadenFroyda

STRAX: XZSwKL8xB3CbKB4Sua5yqNzNm9PeKG1xJN

version: 2.0

---
A script, based on [pystratis](http://github.com/stratisproject/pystratis), for automating the transfer of CIRRUS masternode rewards to STRAX mainchain.
- **Validates crosschain address to prevent errors!**
- Tries to send transaction with lowest possible fee.
- Transfers funds every 6 hours (change with `HOURS_BETWEEN_CONSOLIDATIONS`)

***Tested and working, but use at your own risk!!!!!***

#### Usage
```commandline
python transfer_masternode_reward_to_mainchain.py [--simulate] [--help]
```

Required non-standard modules (pip install <module>):

- pystratis 
- python-decouple
- cryptography
 
### Notes

The following variables must be set in a file named .env in the same folder as this module. 
```text
SENDING_ADDRESS='<YOUR SENDING ADDRESS HERE>'
MAINCHAIN_ADDRESS='<YOUR MAINCHAIN ADDRESS HERE>'
```
OR
    
Modify the following two statements in `transfer_masternode_reward_to_mainchain.py` as shown in the code below with the respective addresses.
```python
MAINCHAIN_ADDRESS = Address(address='<YOUR MAINCHAIN ADDRESS HERE>', network=StraxMain())
SENDING_ADDRESS = Address(address='<YOUR SENDING ADDRESS HERE>', network=CirrusMain())
```

### Transaction simulation
- Set `--simulate` command line flag 
- During simulation, you can verify important transaction details:
  * **Crosschain transfer address**
  * **Amount being sent** and **multisig federation address**

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

  