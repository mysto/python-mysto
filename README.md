
# mysto - Data Anonymiztion in Python


## Requires

This project was built and tested with Python 3.6 and later versions.  It requires the pycryptodome and ff3 libraries:

`pip3 install pycryptodome`
`pip3 install ff3`

## Installation

Install this project with pip:

`pip3 install core`

## Usage

tbd

## Code Example

The example code below can help you get started.

Using default domain [0-9]
```python3

import main
df=main.load_csv('demo/CCSampleData.csv', {"Zipcode": str}, date_types=['Birth Date'])
df
out_df = main.anonymize(df)
out_df

```
## Testing

To run unit tests on this implementation:

  1. `python3 core_test.py`

## Algorithum Notes


## Implementation Notes

## Author

Brad Schoening

## License

This project is licensed under the terms of the [Server Side Pubic License](https://www.mongodb.com/licensing/server-side-public-license).
