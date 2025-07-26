import re
import numpy as np
import pandas as pd
from typing import Tuple, Union

def clean_score(raw_score: Union[str, float, int]) -> Tuple[Union[float, None], str]:
    if pd.isna(raw_score) or str(raw_score).strip().lower() in ['nan', 'none', '']:
        return None, 'C'

    if isinstance(raw_score, (int, float)):
        return float(raw_score), 'A'
    
    score_str = str(raw_score).strip()

    if score_str.lower().startswith('0b'):
        try:
            cleaned = int(score_str, 2)
            return float(cleaned), 'B'
        except ValueError:
            pass

    correction_map = str.maketrans({
        'O': '0', 'o': '0',
        'l': '1', 'I': '1',
        'B': '8'
    })
    corrected = score_str.translate(correction_map)
    
    def extract_single_number_with_span(s: str) -> Tuple[Union[float, None], Union[str, None], Union[Tuple[int, int], None]]:
        matches = list(re.finditer(r'\d+', s)) # 100sp

        # text = 'score: 100jum'
        # m = re.search(r'\d+', text) # to find the first number set
        # print(m.group()) # "100"

        if len(matches) == 1:
            try:
                val_str = matches[0].group()
                span = matches[0].span()
                val = float(val_str)
                if 0 < val <= 100:
                    return val, val_str, span
            except:
                pass
        return None, None, None
    
    val_orig, str_orig, span_orgi = extract_single_number_with_span(score_str)
    val_corr, str_corr, span_corr = extract_single_number_with_span(corrected)

    if val_corr is not None:
        if score_str != corrected: # 1OO
                                   # 100
            if val_orig is None:
                return val_corr, 'B'
        
            if span_orgi == span_corr:
                slice_orig = score_str[span_orgi[0]:span_orgi[1]]
                slice_corr = corrected[span_corr[0]:span_corr[1]]
                if slice_orig == slice_corr:
                    return val_corr, 'A'
                else:
                    return val_corr, 'B'
            else:
                return val_corr, 'B'
        else:
            return val_corr, 'A'
    elif val_orig is not None:
        return val_orig, 'A'
    
    return None, 'C'