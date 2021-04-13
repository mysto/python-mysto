"""
Copyright 2021 Schoening Consulting, LLC
"""

import json
import pandas as pd
from collections import namedtuple
import logging
from ff3 import FF3Cipher
from rules import clipl, date_generalize, fpe, redact, us_zipcode

# display data set on CLI
def display_df(dframe):
    pd.set_option("display.max_columns", 12)
    pd.set_option("display.width", 120)
    print(dframe)
    dframe

def load_csv(fname, dtype={}, date_types=[]):
    # turn off NA filter so that missing values don't become NaN
    # df=pd.read_csv('demo/CCSampleData.csv', dtype={"Zipcode": str}, parse_dates=dtypes, na_filter=False)
    print(date_types)
    df=pd.read_csv(fname, dtype={"Zipcode": str}, parse_dates=date_types, na_filter=False)
    return df

# TODO: refactor global 
date_types = []


class Cipher:
    instance = None


def initialize_fpe(key, tweak, radix = 10):
    Cipher.instance = FF3Cipher(key, tweak, radix)

def old_anonymize(df):
    # for now, read rules from here instead of .deid file

    deid = [
        '{"column" : "First name", "type" : "clipl", "n" : "1"}',
        '{"column" : "Last name", "type" : "clipl", "n" : "3"}',
        '{"column" : "Zipcode", "type" : "us_zipcode"}',
        '{"column" : "SSN", "type" : "FF3", "format" : "000-00-0000", "sep" : "-"}',
        '{"column" : "Canadian SIN", "type" : "FF3", "format" : "000-000-000"}',
        '{"column" : "Employee ID", "type" : "redact"}',
        '{"column" : "Birth Date", "type" : "Generalize.Date", "format" : "5"}',
        '{"column" : "Acct num", "type" : "Mask", "format" : "5"}'
    ]
    return anonymize(df, deid)

def build_rules(rules):
    rulemap = {}

    for row in rules:
        # map each row in deid to a tuple
        x = json.loads(row, object_hook= lambda d: namedtuple('X', d.keys()) (*d.values()))
        if x.type == "FF3":
             obj = lambda s: fpe(Cipher.instance,s)
        elif x.type == "Generalize.Date":
            # obj = lambda x: datetime.date(x.year, 1, 1)
            obj = lambda x: date_generalize(x)
            date_types.append(x.column)
        elif x.type == "Mask":
            width = int(x.format)
            obj = lambda s: len(s[:-width])*"#"+s[-width:]
        elif x.type == "us_zipcode":
            obj = lambda s: us_zipcode(s)
        elif x.type == "clipl":
            lm = lambda n: lambda s: clipl(s,int(n))
            obj = lm(x.n)
        elif x.type == "redact":
            obj = lambda s: redact(s)
        else:
            raise ValueError(f"Unexpected rule {x.type}")
        rulemap[x.column] = obj

    #print(rulemap)
    #print(date_types)
    return rulemap

def anonymize(df, rulelist):

    # Data rules require type coercion by pandas read_csv
    # date_rules = { "Generalize.Date" }

    df = df.copy()
    rulemap = build_rules(rulelist)

    # iterate over the bound rules, appying them to columns
    for colname, functor in rulemap.items():
        if colname in df.columns:
            logging.info("anonymize %s", colname)
            df[colname] = df[colname].apply(rulemap[colname])
        else:
            logging.warning("missing column %s", colname)

    print(f"processed {df.shape[0]} rows")
    return df

if __name__ == "__main__":
    # TODO: read rules for csv data types
    df=load_csv('../demo/CCSampleData.csv', {"Zipcode": str}, date_types=['Birth Date'])
    # TODO: refactor into load rules and process data
    out_df = anonymize(df)
    display_df(df)
    df.to_csv('../demo/CCSampleDataOut.csv')
