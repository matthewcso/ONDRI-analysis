import re
from io import StringIO
import pandas as pd
def asegStats_to_df(path):
    def _replace_spaces_with_comma(x):
        return re.sub('[^\S\n]{1,}', ',', x)

    def _is_table(x):
        if len(x) == 0:
            return False
        elif x[0] == '#':
            return False
        else:
            return True
    
    header = 'Index SegId NVoxels Volume_mm3 StructName normMean normStdDev normMin normMax normRange'

    with open(path, 'r') as r:
        f = r.read()



    table_raw = list(filter(_is_table, f.split('\n')))
    table_raw.insert(0, header)
    table_raw = [x.strip() for x in table_raw]
    table_raw = '\n'.join(table_raw)
    table_raw = _replace_spaces_with_comma(table_raw)
    return pd.read_csv(StringIO(table_raw))