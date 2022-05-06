# https://github.com/Unbabel/COMET

comet-score --model wmt21-comet-qe-mqm -s ted_data/test.en -t ted_data/test.ar > en_ar_raw

cut -d " " -f 3 en_ar_raw > en_ar

comet-score --model wmt21-comet-qe-mqm -s ted_data/test.en -t ted_data/test.de > en_de_raw

cut -d " " -f 3 en_de_raw > en_de

comet-score --model wmt21-comet-qe-mqm -s ted_data/test.en -t ted_data/test.es > en_es_raw

cut -d " " -f 3 en_es_raw > en_es

comet-score --model wmt21-comet-qe-mqm -s ted_data/test.en -t ted_data/test.fr > en_fr_raw

cut -d " " -f 3 en_fr_raw > en_fr

comet-score --model wmt21-comet-qe-mqm -s ted_data/test.en -t ted_data/test.he > en_he_raw

cut -d " " -f 3 en_he_raw > en_he

comet-score --model wmt21-comet-qe-mqm -s ted_data/test.en -t ted_data/test.it > en_it_raw

cut -d " " -f 3 en_it_raw > en_it

comet-score --model wmt21-comet-qe-mqm -s ted_data/test.en -t ted_data/test.ja > en_ja_raw

cut -d " " -f 3 en_ja_raw > en_ja

comet-score --model wmt21-comet-qe-mqm -s ted_data/test.en -t ted_data/test.ko > en_ko_raw

cut -d " " -f 3 en_ko_raw > en_ko

comet-score --model wmt21-comet-qe-mqm -s ted_data/test.en -t ted_data/test.nl > en_nl_raw

cut -d " " -f 3 en_nl_raw > en_nl

comet-score --model wmt21-comet-qe-mqm -s ted_data/test.en -t ted_data/test.pt_br > en_pt_br_raw

cut -d " " -f 3 en_pt_br_raw > en_pt_br

comet-score --model wmt21-comet-qe-mqm -s ted_data/test.en -t ted_data/test.ro > en_ro_raw

cut -d " " -f 3 en_ro_raw > en_ro

comet-score --model wmt21-comet-qe-mqm -s ted_data/test.en -t ted_data/test.ru > en_ru_raw

cut -d " " -f 3 en_ru_raw > en_ru

comet-score --model wmt21-comet-qe-mqm -s ted_data/test.en -t ted_data/test.tr > en_tr_raw

cut -d " " -f 3 en_tr_raw > en_tr

comet-score --model wmt21-comet-qe-mqm -s ted_data/test.en -t ted_data/test.zh_cn > en_zh_cn_raw

cut -d " " -f 3 en_zh_cn_raw > en_zh_cn