import pandas as pd
import re
from typing import Tuple, Union

ENGNLISH_TO_NUM = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'twenty-one': 21,
    'twenty-two': 22,
    'twenty-three': 23,
    'twenty-four': 24,
    'twenty-five': 25,
}

def clean_age(raw_age: Union[str, float, int]) -> Tuple[Union[float, None], str]:
    if pd.isna(raw_age) or str(raw_age).strip().lower() in ['', 'n/a', '-', 'none']:
        return None, 'C'
    
    age_str = str(raw_age).strip().lower()

    if age_str.startswith('0x'):
        try:
            val = int(age_str, 16)
            if 0 <= val <= 100:
                return float(val), 'B'
        except ValueError:
            pass
    
    if age_str in ENGNLISH_TO_NUM:
        return float(ENGNLISH_TO_NUM[age_str]), 'B'
    
    match = re.search(r'\d{1,3}', age_str)
    if match:
        try:
            val = float(match.group())
            if 0 <= val <= 100:
                return val, 'A'
        except:
            pass

    return None, 'C'

