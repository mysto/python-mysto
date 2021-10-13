# Data anonymization with python Mysto

In this tutorial, we'll use Mysto to anonymize columuns in a sample data set.  

Prerequisites:
* Python3
* The following Python packages are required:
    * pandas (pip3 install pandas)
    * pycryptodome (pip3 install pycryptodome)
    * ff3  (pip3 install ff3)

This tutorial is paired with a Jupyter notebook file, but
it can be run just fine from the command line also.

To begin with, start a Jupyter notebook using the tutorial file 
```
jupyter notebook MystoTutorial.ipynb &
```
As a first step, load the sample CSV file. We use the Pandas CSV reader
which provides excellent handling of data types, especially dates.

```
df=main.load_csv('https://raw.githubusercontent.com/mysto/python-mysto/main/samples/CCSampleData.csv', {"Zipcode": str}, date_types=['Birth Date'])
```

1. Define HIPAA rules for generalizing zipcode and birth date colums
```python
rules = [
    '{"column" : "Zipcode", "type" : "us_zip_code"}',
    '{"column" : "Birth Date", "type" : "Generalize.Date", "format" : "5"}',
]

df1 = main.anonymize(df, rules)
df1
```

In the output you'll see for zipcode, last two digit are generalized with zeros and birth date 
has been generalized to year.

2. Next we'll add rules to *clip* first and last name and *mask* the account number

```python
rules = [
    '{"column" : "Zipcode", "type" : "us_zip_code"}',
    '{"column" : "Birth Date", "type" : "Generalize.Date", "format" : "5"}',
    
    '{"column" : "First name", "type" : "clipl", "n" : "1"}',
    '{"column" : "Last name", "type" : "clipl", "n" : "3"}',
    '{"column" : "Acct num", "type" : "Mask", "format" : "5"}'
]

df2 = main.anonymize(df, rules)
df2
```

3. Finally, we will tokenize the SSN and CSN columns with format-preserving encryption 
and redact the account number column.

```sh
rules = [
    '{"column" : "Zipcode", "type" : "us_zip_code"}',
    '{"column" : "Birth Date", "type" : "Generalize.Date", "format" : "5"}',
    
    '{"column" : "First name", "type" : "clipl", "n" : "1"}',
    '{"column" : "Last name", "type" : "clipl", "n" : "3"}',
    '{"column" : "Acct num", "type" : "Mask", "format" : "5"}',
    
    '{"column" : "SSN", "type" : "FF3", "format" : "000-00-0000", "sep" : "-"}',
    '{"column" : "Canadian SIN", "type" : "FF3", "format" : "000-000-000"}',
    '{"column" : "Acct num", "type" : "Mask", "format" : "5"}'
]

main.initialize_fpe("EF4359D8D580AA4F7F036D6F04FC6A94", "D8E7920AFA330A73")

df3 = main.anonymize(df, rules)
df3
```
