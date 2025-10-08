#python

#File:        encryption_admin.py
#Author:      u112000
#Created:     2025-10-08

#License:     MIT License — see LICENSE file in repository
#Repository:  https://github.com/u112000

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets
import base64

def encryptor(subject, body, status, type):
    from package.core import _key, _nonce, _aad
    SUBJECT = subject.encode()
    BODY =  body.encode() 
    STATUS = status.encode()

    key = secrets.token_bytes(32)
    nonce = secrets.token_bytes(12)
    aad = secrets.token_bytes(12)
    aesgcm = AESGCM(key)

    sub_ = aesgcm.encrypt(nonce, SUBJECT, aad)
    body_ = aesgcm.encrypt(nonce, BODY, aad)
    stat_ = 'ENCRYPTED'
    if type == 's':
        return (sub_.hex(), body_.hex(), stat_, key.hex(), nonce.hex(), aad.hex())

    elif type == 'a':
        key = _key
        nonce = _nonce
        aad = _aad
        aesgcm = AESGCM(key)

        sub_ = aesgcm.encrypt(nonce, SUBJECT, aad)
        body_ = aesgcm.encrypt(nonce, BODY, aad)
        stat_ = 'ENCRYPTED'
        return (sub_.hex(), body_.hex(), stat_)


def Decryptor(key, nonce, aad, sub, body):
    try:
        key_ = bytes.fromhex(key)
        nonce_ = bytes.fromhex(nonce)
        aad_ = bytes.fromhex(aad)
        aesgcm = AESGCM(key_)
    
        subject_ = bytes.fromhex(sub)
        body_ = bytes.fromhex(body)

        status = 'NOT-ENCRYPTED'
        SUBJECT = aesgcm.decrypt(nonce_, subject_, aad_)
        BODY = aesgcm.decrypt(nonce_, body_, aad_)
    except:
        return 'ERROR'
    else:
        return (SUBJECT.decode(), BODY.decode(), status)
