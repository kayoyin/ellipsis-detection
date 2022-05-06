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
                        if p[i] == row.split(':')[0]:
                            if float(row.split(' ')[-1]) > top:
                                top = float(row.split(' ')[-1])
                                top_x = span
            f.close()

            print(p[i] + ' ' + measure + ' ' + lang)
            print(top_x)
            print(top)
