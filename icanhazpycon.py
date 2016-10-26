
import sys
import hashlib
import time
import binascii

import requests

registration_url = 'https://us.pycon.org/2017/registration'
hash_file_path = 'hash.txt'


def get_hash(url):
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        s = "can't connect to the internet - sorry - exiting"
        print(s)
        sys.exit(s)
    h = hashlib.md5()
    h.update(r.text.encode())
    hash_string = str(binascii.b2a_hex(h.digest()))
    write_hash(hash_string)
    return hash_string


def beep():
    sys.stdout.write('\a')
    sys.stdout.flush()
    time.sleep(0.5)


def write_hash(hash_string):
    with open(hash_file_path, 'w') as f:
        f.write(hash_string)


def read_hash():
    try:
        with open(hash_file_path) as f:
            s = f.readline().strip()
    except FileNotFoundError:
        s = None
    print('read_hash : %s' % s)
    return s


def main():

    [beep() for _ in range(0,3)]
    sleep_time = 5 * 60

    new_hash = get_hash(registration_url)
    prior_hash = read_hash()  # in case the page has changed since we last ran this program
    if prior_hash is None:
        prior_hash = new_hash  # first time assume it's still pending
    while new_hash == prior_hash:
        print('%s has md5 of %s - sleeping for %d' % (registration_url, new_hash, sleep_time))
        time.sleep(sleep_time)
        prior_hash = new_hash
        new_hash = get_hash(registration_url)

    print('go now!')
    print(registration_url)
    for _ in range(0,999):
        beep()

if __name__ == '__main__':
    main()
