import pandas as pd

example_stats = pd.read_csv('utils/example_fs_stats.stats', sep='\s+')
total_lookup=dict(zip(example_stats['SegId'], example_stats['StructName']))


simplified_lookup_numeric = {}
for key, value in total_lookup.items():
    if 'White-Matter' in value:
        simplified_lookup_numeric[key] = 1

    elif 'ctx' in value or 'CC' in value:
        simplified_lookup_numeric[key] = 2


example_ctx_stats = pd.read_csv('utils/example_fs_stats_ctx.stats', sep='\s+')
example_ctx_stats = example_ctx_stats[example_ctx_stats['subtype'] != '-']
unique_ctx = example_ctx_stats['subtype'].unique()
