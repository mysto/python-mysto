
# mysto - Data Anonymization in Python


## Requires

This project was built and tested with Python 3.6 and later versions.  It requires the pycryptodome and ff3 libraries:

`pip3 install pycryptodome`
`pip3 install ff3`

## Installation

Install this project with pip:

`pip3 install mysto`

## Usage

The Mysto toolkit provides an integrated de-identification solution, including:
* Date generalization
* Format-preserving encryption (FPE) for alphanumerics
* Masking, including customized rules for US SSN  
* HIPAA compliant date and zip code rules

## Code Example

The code example below can help you get started:

```python3
import pandas as pd
from datetime import date
import main 

d = {'SSN': ['938-49-5100', '976-52-7639'], 'date': [date(1994,2,22), date(2000,10,10)]}
df = pd.DataFrame(data=d)
rules = [ '{"column" : "SSN", "type" : "Mask", "format" : "5" }',  '{"column" : "date", "type" : "Generalize.Date"}' ]
out_df = main.anonymize(df, rules)
print(out_df)
```
## Testing

To run unit tests on this implementation:

  1. `python3 rules_test.py`

## Implementation Notes

## Author

Brad Schoening

## License

This project is licensed under the terms of the [Server Side Pubic License](https://www.mongodb.com/licensing/server-side-public-license).
