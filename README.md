# Multi^2OIE: <u>Multi</u>lingual Open Information Extraction Based on <u>Multi</u>-Head Attention with BERT

> Source code for learning Multi^2OIE for (multilingual) open information extraction.

<b>NOTE:</b> This is not the original repository, I clone it to modify it to be able to train the model in Google Colab, in particular for the Spanish language.

## Paper
[**Multi^2OIE: <u>Multi</u>lingual Open Information Extraction Based on <u>Multi</u>-Head Attention with BERT**](https://arxiv.org/abs/2009.08128)<br>
[Youngbin Ro](https://github.com/youngbin-ro), [Yukyung Lee](https://github.com/yukyunglee), and [Pilsung Kang](https://github.com/pilsung-kang)*<br>
Accepted to Findings of ACL: EMNLP 2020. (*corresponding author)

<br>

## Overview
### What is Open Information Extraction (Open IE)?
[Niklaus et al. (2018)](https://www.aclweb.org/anthology/C18-1326/) describes Open IE as follows:

> Information extraction (IE) **<u>turns the unstructured information expressed in natural language text into a structured representation</u>** in the form of relational tuples consisting of a set of arguments and a phrase denoting a semantic relation between them: <arg1; rel; arg2>. (...) Unlike traditional IE methods, Open IE is **<u>not limited to a small set of target relations</u>** known in advance, but rather extracts all types of relations found in a text.

![openie_overview](https://github.com/youngbin-ro/Multi2OIE/blob/master/images/openie_overview.PNG?raw=true)

#### Note
- Systems adopting sequence generation scheme ([Cui et al., 2018](https://www.aclweb.org/anthology/P18-2065/); [Kolluru et al., 2020](https://www.aclweb.org/anthology/2020.acl-main.521/)) can extract (actually generate) relations outside of given texts.
- Multi^2OIE, however, is adopting sequence labeling scheme ([Stanovsky et al., 2018](https://www.aclweb.org/anthology/N18-1081/)) for computational efficiency and multilingual ability



### Our Approach

![multi2oie_overview](https://github.com/youngbin-ro/Multi2OIE/blob/master/images/multi2oie_overview.PNG?raw=true)

#### Step 1: Extract predicates (relations) from the input sentence using BERT
- Conduct token-level classification on the BERT output sequence
  - Use BIO Tagging for representing arguments and predicates

#### Step 2: Extract arguments using multi-head attention blocks
- Concatenate BERT whole hidden sequence, average vector of hidden sequence at predicate position, and binary embedding vector indicating the token is included in predicate span.
- Apply multi-head attention operation over N times
    - Query: whole hidden sequence
    - Key-Value pairs: hidden states of predicate positions
- Conduct token-level classification on the multi-head attention output sequence

#### Multilingual Extraction

- Replace English BERT to Multilingual BERT
- Train the model only with English data
- Test the model in three difference languages (English, Spanish, and Portuguese) in zero-shot manner.

<br>


## Usage

### Prerequisites

- Python 3.7

- CUDA 10.0 or above

### Environmental Setup

##### using  'conda' command,
~~~~
# this makes a new conda environment
conda env create -f environment.yml
conda activate multi2oie
~~~~

##### using  'pip' command,
~~~~
pip install -r requirements.txt
~~~~

### Datasets

Original data file (bootstrapped sample from OpenIE4; used in SpanOIE) can be downloaded from [here](https://drive.google.com/file/d/1AEfwbh3BQnsv2VM977cS4tEoldrayKB6/view).
Following download, put the downloaded data in './datasets' and use preprocess.py to convert the data into the format suitable for Multi^2OIE. See below: 

~~~~
cd utils
python preprocess.py \
    --mode 'train' \
    --data '../datasets/structured_data.json' \
    --save_path '../datasets/openie4_train.pkl' \
    --bert_config 'bert-base-cased' \
    --max_len 64
~~~~

For multilingual training data, set **'bert_config'** as **'bert-base-multilingual-cased'**. 

### download stopwords from nltk
Open Python 3 console
~~~~
import nltk
nltk.download('stopwords')
~~~~

### Run the Code

We used TITAN RTX GPU for training, and the use of other GPU can make the final performance different.
ALso it could be trained in Google colab.

##### for training,

~~~~
python main.py [--FLAGS]
~~~~

##### for testing,

~~~~
python test.py [--FLAGS]
~~~~

<br>

## Model Configurations

### # of Parameters

- Original BERT: 110M
- \+ Multi-Head Attention Blocks: 66M



### Hyper-parameters {& searching bounds}

- epochs: 1 {**1**, 2, 3}
- dropout rate for multi-head attention blocks: 0.2 {0.0, 0.1, **0.2**}
- dropout rate for argument classifier: 0.2 {0.0, 0.1, **0.2**, 0.3}
- batch size: 128 {64, **128**, 256, 512}
- learning rate: 3e-5 {2e-5, **3e-5**, 5e-5}
- number of multi-head attention heads: 8 {4, **8**}
- number of multi-head attention blocks: 4 {2, **4**, 8}
- position embedding dimension: 64 {**64**, 128, 256}
- gradient clipping norm: 1.0 (not tuned)
- learning rate warm-up steps: 10% of total steps (not tuned)

<br>

## Expected Results

### Development set

#### OIE2016

- F1: 71.7
- AUC: 55.4

#### CaRB

- F1: 54.3
- AUC: 34.8



### Testing set

#### Re-OIE2016

- F1: 83.9
- AUC: 74.6

#### CaRB

- F1: 52.3
- AUC: 32.6

<br>

## References

- https://github.com/gabrielStanovsky/oie-benchmark
- https://github.com/dair-iitd/CaRB
- https://github.com/zhanjunlang/Span_OIE

## Run with other datasets:

1. create a json file with an array of sentences
2. Use datasets/pickleCreator.py to convert the JSON file into pickle file
3. Execute test.py with test_data_path to the picke file:
~~~~
python3 test.py --test_data_path ./datasets/spanish_corpus_testset_rodriguez.pkl
~~~~
