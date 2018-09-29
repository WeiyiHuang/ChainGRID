import pexpect

def key_gen(usr_name):
    

def open_cli(usr_name):
    w = ['./bin/mktclient', '--name', usr_name, '--keyfile', 'validator/keys/%s.wif'%usr_name]
    p = pexpect.spawn(' '.join(w))
    print('Client for %s opened.'%usr_name)
    return p

def close_cli(process, usr_name):
    p.close(force=True)
    print('Client for %s closed.'%usr_name)

if __name__ == '__main__':
    usr_cli_dict = {}
    usr_cli_dict['bob'] = open_cli('bob')
    p = usr_cli_dict.get('bob')
    index = p.expect([
        'bob>',
    ])
    if index == 0:
        print ("Login to mkt")
    p.sendline('waitforcommit')
    p.expect('No transaction specified to wait for.')
    print('lalal')
    p.sendline('offers --creator //bob')
    p.expect('0.5')
    print('offer found')
    p.interact()
    p.close(force=True)
    

