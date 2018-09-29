import pexpect
import subprocess

def key_gen(usr_name):
    w = ['./bin/sawtooth', 'keygen', '--key-dir', 'validator/keys', usr_name]
    p = subprocess.call(w)
    print('Key for %s is generated'%usr_name)

def open_cli(usr_name):
    w = ['./bin/mktclient', '--name', usr_name, '--keyfile', 'validator/keys/%s.wif'%usr_name]
    p = pexpect.spawn(' '.join(w))
    print('Client for %s opened.'%usr_name)
    return p

def close_cli(process, usr_name):
    process.close(force=True)
    print('Client for %s closed.'%usr_name)

def standard_interaction(process, sentence):
    idx = process.expect(['submitted','failed to create transaction'], timeout=100, searchwindowsize=100)
    if idx:
        print('T_TFailed to create transaction. ==>%s'%sentence)
    else:
        print('@_@Transaction submitted. ==>%s'%sentence)

def standard_input(process, sentence):
    process.sendline(sentence)
    standard_interaction(process, sentence)

def mining(process):
    process.sendline('waitforcommit')
    idx = process.expect(['Transaction committed.', 'No transaction specified to wait for.'], timeout=300, searchwindowsize=100)
    if idx:
        print('=_=No transaction specified to wait for.')
    else:
        print('$$$Mined!')
    
def register_participant_account(process, usr_name):
    standard_input(process, 'participant reg --name %s'%usr_name)
    standard_input(process, 'account reg --name /account')
    mining(process)
    standard_input(process, 'holding reg --name /USD --account /account --asset //mkt/asset/currency/USD')
    standard_input(process, 'holding reg --name /holding/token --count 1 --account /account --asset //marketplace/asset/token')
    mining(process)
    standard_input(process, 'exchange --type SellOffer --src /holding/token --dst /USD --offers //mkt/offer/provision/USD --count 1')
    standard_input(process, 'holding reg --name /jars/choc_chip --account /account --asset //mkt/asset/cookie/choc_chip')
    mining(process)
    print('Register the participant and account.')
    

if __name__ == '__main__':
    usr_name = 'test_6'
    key_gen(usr_name)
    p = open_cli(usr_name)
    register_participant_account(p, usr_name)
    
    close_cli(p, usr_name)
    #usr_cli_dict = {}
    #usr_cli_dict['bob'] = open_cli('bob')
    #p = usr_cli_dict.get('bob')
