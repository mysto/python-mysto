"""
Copyright 2021 Schoening Consulting, LLC
"""

import re
import datetime

def clipl(s, n):
    """
    Clip a string on the left to the n right-most characters 
    """
    return s[:n]

def clipr(s, n):
    """
    Clip a string on the right to the n right-most characters 
    """
    return s[len(s)-n:]

def date_generalize(dt):
    """
    Generalize a date to a year
    """
    return datetime.date(dt.year, 1, 1)

def fpe(c, s):
    """
    Return a format preserving encrypted value
    """
    # print(s,type(s)) 
    if not isinstance(s, str) or len(s) < 2:
        # Original FF3 minLen was 2
        # TODO: compare c.minLen instead of constant, add test cases
        # raise ValueError(f'length {len(s)}, but fpe requires 3 or more')
        return "" 
    a = re.sub(r"[^\d]", "", s)
    res = c.encrypt(a)
    return res

def mask(s, width, mchar="X"):
    """
    Return a string masking all but the last width characters
    """
    return len(s[:-width]) * mchar + s[-width:]

def mask_ssn(s, mchar="X"):
    """
    Mask US SSN with separators intact
    """
    return mchar*3 + '-' + mchar*2 + '-' + s[-4:]

def redact(s):
    return ""

zip_blacklist = ('03600', '05900', '06300', '10200', '20300', '55600', '69200', '79000',
                 '82100', '82300', '83000', '83100', '87800', '87900', '88400', '89000', '89300')

def us_zipcode(zipcode: str) -> str:
    """
    Return a five digit zipcode with the last two digits replaced by zeros.
    Input may be either a five digit or 9 digit zip+4
    """
    if len(zipcode) not in (5, 10):
        raise ValueError(f'zipcode length was {len(zipcode)}, but valid zipcodes are 5 or 10 digits')
    newz = zipcode[0:3] + '00'
    if newz in zip_blacklist:
        return '00000'
    else:
        return newz
