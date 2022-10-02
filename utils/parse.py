import glob
import pandas as pd
from collections import defaultdict
from pathlib import Path

def parse_file_name(name):
    split = name.split("_")
    value = split[-1]
    offset = split[-2].split("kb")[0]
    windowsize = split[-3].split("kg")[0]
    binsize = split[-4].split("kb")[0]
    region = "_".join(split[:-4])
    return region, binsize, windowsize, offset, value

def recDict():
    """Recursive defaultdict that allows deep
    assignment. recDict[0][1][2] will
    create all intermediate dictionaries."""
    return defaultdict(recDict)

def parse_directory(dir):
    files = glob.glob(str(Path(dir) / "*.csv"))
    output = recDict()
    for file in files:
        region, binsize, _, offset, value = parse_file_name(Path(file).name.split(".")[0])
        output[region][binsize][offset][value] = pd.read_csv(file, index_col=0)
    return output