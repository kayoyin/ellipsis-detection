import pandas as pd

def spanner(d):
    spanned_dict = {}
    for key in d.keys():
        key_span = []
        potential_span = []
        for i in range(len(d[key])):
            if i == 0:
                potential_span.append(d[key][i])
            else:
                if d[key][i] - 1 == potential_span[-1]:
                    potential_span.append(d[key][i])
                else:
                    if potential_span:
                        key_span.append(potential_span)
                    potential_span = [d[key][i]]
        if potential_span:
            key_span.append(potential_span)
        spanned_dict[key] = key_span

    return spanned_dict

y = open('results.txt', 'w')

for l in ['fr', 'ja', 'zh_cn']:
    for m in ['comet.', 'prism.', 'tedref.']:
        thres = []
        if m == 'comet.':
            thres = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19]
        elif m == 'prism.':
            thres = [-8.0, -7.5, -7.0, -6.5, -6.0, -5.5, -5.0, -4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5]
        else:
            thres = [0]

        for t in thres:

            tokens_file = open('newtokens/test.tok.' + l)

            if m != 'tedref.':
                # model tags
                tags_file = open('tags_with_thresh/' + m + str(t) + '.' + l)
            else:
                # baseline tags
                tags_file = open('tags_with_thresh/' + m + l)

            print('tags_with_thresh/' + m + str(t) + '.' + l)

            tokens = []
            for line in tokens_file:
                tokens.append(line.strip())

            tags = []
            for line in tags_file:
                tags.append(line.strip())

            indices_of_true = []
            df = pd.read_csv(open('english.tsv'), delimiter='\t', low_memory=False)

            indices_of_true = df[df['Ellipsis (0 = no, 1 = yes)'] == 1].index.tolist()

            # all that are labeled as correct -> newtags
            # utt: [token #1, token #2, etc]
            labeled_correct = {}
            for i in range(len(tags)):
                ellided_tks = []
                for j in range(len(tags[i].split(' '))):
                    x = tags[i].split(' ')[j].split('+')
                    if 'ellipsis' in x:
                        ellided_tks.append(j)
                if ellided_tks:
                    labeled_correct[i] = ellided_tks.copy()

            # filter for the sentences with actual ellipses
            true_file = pd.read_csv(open('ellipsis_tag2.tsv'), delimiter='\t')
            potential_elided = true_file[l].values

            actual_elided = {}
            for i in range(len(potential_elided)):
                if not pd.isna(potential_elided[i]):
                    if '{{' in potential_elided[i] and '}}' in potential_elided[i]:
                        tokenized = tokens[indices_of_true[i]]
                        need_tokenized = potential_elided[i]

                        need_tokenized_split = None
                        if l == 'fr':
                            need_tokenized_split = need_tokenized.split(' ')
                        elif l == 'ja' or l == 'zh_cn':
                            need_tokenized_split = []
                            for tk in need_tokenized:
                                if tk == '{':
                                    try:
                                        if need_tokenized_split[-1] == '{':
                                            need_tokenized_split[-1] = '{{'
                                        else:
                                            need_tokenized_split.append(tk)
                                    except IndexError:
                                        need_tokenized_split.append(tk)
                                elif tk == '}':
                                    try:
                                        if need_tokenized_split[-1] == '}':
                                            need_tokenized_split[-1] = '}}'
                                        else:
                                            need_tokenized_split.append(tk)
                                    except IndexError:
                                        need_tokenized_split.append(tk)
                                else:
                                    need_tokenized_split.append(tk)

                        if l == 'ja' or l == 'zh_cn':
                            all_elide = []
                            is_elide = False
                            for j in range(len(tokenized.split(' '))):
                                while not need_tokenized_split[0]:
                                    need_tokenized_split = need_tokenized_split[1:]

                                compare = need_tokenized_split[0]

                                if compare == '{{':
                                    is_elide = True
                                    need_tokenized_split = need_tokenized_split[1:]
                                    compare = need_tokenized_split[0]
                                elif compare == '}}':
                                    is_elide = False
                                    need_tokenized_split = need_tokenized_split[1:]
                                    compare = need_tokenized_split[0]

                                if compare in tokenized.split(' ')[j]:
                                    compare = ''.join(need_tokenized_split[0:len(tokenized.split(' ')[j])])
                                    
                                if tokenized.split(' ')[j] == compare:
                                    need_tokenized_split = need_tokenized_split[len(tokenized.split(' ')[j]):]
                                else:
                                    need_tokenized_split[0] = need_tokenized_split[0].replace(tokenized.split(' ')[j], '')

                                if is_elide:
                                    all_elide.append(j)

                            if all_elide:
                                actual_elided[indices_of_true[i]] = all_elide.copy()
                        elif l == 'fr':
                            all_elide = []
                            is_elide = False
                            for j in range(len(tokenized.split(' '))):
                                while not need_tokenized_split[0]:
                                    need_tokenized_split = need_tokenized_split[1:]

                                compare = need_tokenized_split[0]

                                if compare == '{{':
                                    is_elide = True
                                    need_tokenized_split = need_tokenized_split[1:]
                                elif compare == '}}':
                                    is_elide = False
                                    need_tokenized_split = need_tokenized_split[1:]

                                if tokenized.split(' ')[j] == compare:
                                    need_tokenized_split = need_tokenized_split[1:]
                                else:
                                    need_tokenized_split[0] = need_tokenized_split[0].replace(tokenized.split(' ')[j], '')

                                if is_elide:
                                    all_elide.append(j)

                            if all_elide:
                                actual_elided[indices_of_true[i]] = all_elide.copy()

            # calculate span overlap precision and recall
            labeled_correct_span = spanner(labeled_correct)
            actual_elided_span = spanner(actual_elided)

            correct_elided = {}
            for key in labeled_correct.keys():
                if key in actual_elided:
                    overlap = []
                    for val in labeled_correct[key]:
                        if val in actual_elided[key]:
                            overlap.append(val)
                    if overlap:
                        correct_elided[key] = overlap

            # all labeled as correct: labeled_correct
            # all that should have been labeled as correct: actual_elided
            # correct: correct_elided

            labeled_correct_count = 0
            for key in labeled_correct.keys():
                labeled_correct_count += len(labeled_correct[key])
            actual_elided_count = 0
            for key in actual_elided.keys():
                actual_elided_count += len(actual_elided[key])
            correct_elided_count = 0
            for key in correct_elided.keys():
                correct_elided_count += len(correct_elided[key])

            y.write('Language: ' + l + ' comparison: ' + m + ' threshold: ' + str(t) + '\n')

            # by token
            # precision
            # (correct)/all labeled as correct
            # print('precision: ', correct_elided_count/labeled_correct_count)
            try:
                y.write('precision: ' + str(correct_elided_count/labeled_correct_count) + '\n')
            except:
                pass

            # recall
            # (correct)/all that should have been labeled correct
            try:
                # print('recall: ', correct_elided_count/actual_elided_count)
                y.write('recall: ' + str(correct_elided_count/actual_elided_count) + '\n')
            except:
                pass

            # print('sentence precision: ', len(correct_elided)/len(labeled_correct))
            # print('sentence recall: ', len(correct_elided)/len(actual_elided))
            try:
                y.write('sentence precision: ' + str(len(correct_elided)/len(labeled_correct)) + '\n')
            except:
                pass

            try:
                y.write('sentence recall: ' + str(len(correct_elided)/len(actual_elided)) + '\n')
            except:
                pass

            # print('labeled', labeled_correct)
            # print('gt ', actual_elided)

            # span precision and recall
            correct_elided_span = {}
            for key in labeled_correct_span.keys():
                if key in actual_elided_span:
                    overlap = []
                    for span in labeled_correct_span[key]:
                        span_done = False
                        for i in range(len(actual_elided_span[key])):
                            if len(set(span).intersection(actual_elided_span[key][i])):
                                if not span_done:
                                    overlap.append(span)
                                    span_done = True
                    if overlap:
                        correct_elided_span[key] = overlap

            labeled_correct_span_count = 0
            for key in labeled_correct_span.keys():
                labeled_correct_span_count += len(labeled_correct_span[key])
            actual_elided_span_count = 0
            for key in actual_elided_span.keys():
                actual_elided_span_count += len(actual_elided_span[key])
            correct_elided_span_count = 0
            for key in correct_elided_span.keys():
                correct_elided_span_count += len(correct_elided_span[key])

            # precision
            # (correct)/all labeled as correct
            # print('precision span: ', correct_elided_span_count/labeled_correct_span_count)
            try:
                y.write('precision span: ' + str(correct_elided_span_count/labeled_correct_span_count) + '\n')
            except:
                pass

            # recall
            # (correct)/all that should have been labeled correct
            try:
                # print('recall span: ', correct_elided_span_count/actual_elided_span_count)
                y.write('recall span: ' + str(correct_elided_span_count/actual_elided_span_count) + '\n')
            except:
                pass

            # print('sentence precision span: ', len(correct_elided_span)/len(labeled_correct_span))
            # print('sentence recall span: ', len(correct_elided_span)/len(actual_elided_span))
            try:
                y.write('sentence precision span: ' + str(len(correct_elided_span)/len(labeled_correct_span)) + '\n')
            except:
                pass

            try:
                y.write('sentence recall span: ' + str(len(correct_elided_span)/len(actual_elided_span)) + '\n')
            except:
                pass

            # create file
            # f = open('check_file.txt', 'w')
            # for key in labeled_correct.keys():
            #     if key not in correct_elided.keys():
            #         f.write(df['English sentence'][key] + '\n')
            #         f.write(tokens[key] + '\n')

            #         f.write('. '*len(tokens[key]) + '\n')

            #         model = (['.']*len(tokens[key])).copy()
            #         for i in range(len(labeled_correct[key])):
            #             model[labeled_correct[key][i]] = 'x'
            #         f.write(' '.join(model) + '\n')

            #         f.write('\n')

            # for key in actual_elided.keys():
            #     if key not in correct_elided.keys():
            #         f.write(df['English sentence'][key] + '\n')
            #         f.write(tokens[key] + '\n')

            #         model = (['.']*len(tokens[key])).copy()
            #         for i in range(len(actual_elided[key])):
            #             model[actual_elided[key][i]] = 'x'
            #         f.write(' '.join(model) + '\n')

            #         f.write('. '*len(tokens[key]) + '\n')
            #         f.write('\n')

            # for key in correct_elided.keys():
            #     f.write(df['English sentence'][key] + '\n')
            #     f.write(tokens[key] + '\n')

            #     model = (['.']*len(tokens[key])).copy()
            #     for i in range(len(actual_elided[key])):
            #         model[actual_elided[key][i]] = 'x'
            #     f.write(' '.join(model) + '\n')
                
            #     model = (['.']*len(tokens[key])).copy()
            #     for i in range(len(labeled_correct[key])):
            #         model[labeled_correct[key][i]] = 'x'
            #     f.write(' '.join(model) + '\n')

            #     f.write('\n')