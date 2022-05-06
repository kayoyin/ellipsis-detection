p = ['precision', 'sentence precision', 'precision span', 'sentence precision span', 'recall', 'sentence recall', 'recall span', 'sentence recall span']

for lang in ['fr', 'ja', 'zh_cn']:
    for measure in ['comet', 'prism']:
        for i in range(len(p)):
            top = 0
            top_x = ''
            span = ''
            skip = False

            f = open('results.txt')
            for row in f:
                if 'Language' in row:
                    if lang in row and measure in row:
                        span = row
                        skip = False
                if not skip:
                    if lang in row and measure in row:
                        span = row
                        skip = False
                    elif 'Language' in row:
                        skip = True
                    else:
                        if p[i] == 'precision':
                            if p[i] in row and 'sentence precision' not in row and 'precision span' not in row and 'sentence precision span' not in row:
                                if float(row.split(' ')[-1]) > top:
                                    top = float(row.split(' ')[-1])
                                    top_x = span
                        elif p[i] == 'recall':
                            if p[i] in row and 'sentence recall' not in row and 'recall span' not in row and 'sentence recall span' not in row:
                                if float(row.split(' ')[-1]) > top:
                                    top = float(row.split(' ')[-1])
                                    top_x = span
                        else:
                            if p[i] in row:
                                if float(row.split(' ')[-1]) > top:
                                    top = float(row.split(' ')[-1])
                                    top_x = span
            f.close()

            print(p[i] + ' ' + measure + ' ' + lang)
            print(top_x)
            print(top)
