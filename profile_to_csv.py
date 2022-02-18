# insert filepath of profile.txt to convert to .csv 
filepath = './profiles/fast_gpu_profile_17-02-2022_21_14_00.txt'

with open(filepath, 'r') as in_file:
    contents = in_file.read().split('\n')
    contents = contents[17:]
    contents = [i.split() for i in contents]

    # rejoin function names in positions item[5:] that are split because they contain ','
    for item in contents:
        if len(item[5:]) > 1:
            joined = [' '.join(item[5:])]
            item[5:] = joined

    contents = [','.join(i) for i in contents]

    outpath = filepath[:-3] + 'csv'
    with open(outpath, 'w') as out_file:
        for line in contents:
            out_file.write(line + '\n')
