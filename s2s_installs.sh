# Indic Trans dependencies
git clone https://github.com/AI4Bharat/indicTrans.git

cp indicTrans_setup.py indicTrans/setup.py
cd indicTrans
cp -r model_configs ../
pip install -e .
cd ..
pip install sacremoses pandas mock sacrebleu tensorboardX pyarrow indic-nlp-library
pip install mosestokenizer subword-nmt

git clone https://github.com/Open-Speech-EkStep/fairseq -b v2-hydra
cd fairseq
pip install -e .
cd ..

downloading the IndicTrans en-indic model 
wget https://storage.googleapis.com/vakyaansh-open-models/translation_models/en-indic.zip
unzip en-indic.zip

