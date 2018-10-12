import pexpect
import subprocess

def key_gen(usr_name):
    w = ['../bin/sawtooth', 'keygen', '--key-dir', '../validator/keys', usr_name]
    p = subprocess.call(w)
    print('Key for %s is generated'%usr_name)

def open_cli(usr_name):
    w = ['../bin/mktclient', '--name', usr_name, '--keyfile', '../validator/keys/%s.wif'%usr_name]
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
    standard_input(process, 'holding reg --name /RMB --account /account --asset //mkt/asset/currency/RMB')
    standard_input(process, 'holding reg --name /holding/token --count 1 --account /account --asset //marketplace/asset/token')
    mining(process)
    standard_input(process, 'exchange --type SellOffer --src /holding/token --dst /RMB --offers //mkt/offer/provision/RMB --count 1')
    standard_input(process, 'holding reg --name /jars/choc_chip --account /account --asset //mkt/asset/cookie/choc_chip')
    mining(process)
    print('Register the participant and account.')

def create_exchange_offer(idx, usr_name_seller, num_of_grocery_sell, ratio, usr_name_buyer, num_of_grocery_buy):
    n_ratio = int(1/ratio)
    seller_p = open_cli(usr_name_seller)
    buyer_p = open_cli(usr_name_buyer)

    mining(seller_p)
    standard_input(seller_p, 'holding reg --name /batches/choc_chip00%d --account /account --asset //mkt/asset/cookie/choc_chip --count %d'%(idx, num_of_grocery_sell))
    mining(seller_p)
    standard_input(seller_p, 'exchangeoffer reg --output /batches/choc_chip00%d --input /RMB --ratio %d 1 --name /choc_chip_sale_%d'%(idx, n_ratio, idx))
    mining(seller_p)

    standard_input(buyer_p, 'exchange --type ExchangeOffer --src /RMB --dst /jars/choc_chip --offers //%s/choc_chip_sale --count %d'\
        %(usr_name_seller, num_of_grocery_buy))
    mining(buyer_p)
    
    close_cli(seller_p, usr_name_seller)
    close_cli(buyer_p, usr_name_buyer)
    
    

if __name__ == '__main__':
    usr_name = 'test_8'
    #key_gen(usr_name)
    #p = open_cli(usr_name)
    #register_participant_account(p, usr_name)
    #close_cli(p, usr_name)
    create_exchange_offer('test_8', 10, 0.5, 'test_7', 2)
    #usr_cli_dict = {}
    #usr_cli_dict['bob'] = open_cli('bob')
    #p = usr_cli_dict.get('bob')
