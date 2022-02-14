python infer_wrapper_asr.py \
--model /home/neerajchhimwal/indian_english_model/english_infer.pt \
--dict /home/neerajchhimwal/indian_english_model/dict.ltr.txt \
--cuda t \
--decoder kenlm \
--lexicon /home/neerajchhimwal/indian_english_model/lexicon.lst \
--lm-path /home/neerajchhimwal/indian_english_model/lm.binary \
--half t

