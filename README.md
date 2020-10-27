# CMU 18794 group project
## installation
This repo is tested on Python 3.6.10, PyTorch 1.5.0

You should install [Transformers](https://github.com/huggingface/transformers#installation) from source first in a [virtual environment](https://docs.python.org/3/library/venv.html). 
If you're unfamiliar with Python virtual environments, check out the [user guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

Create a virtual environment with the version of Python (Python 3.6 strongly recommended, or you need to deal with some bugs in python 3.5 and 3.7+ by changing the python source code) you're going to use and activate it.

Here also, you first need to install PyTorch and pandaraller. Please refer to [PyTorch installation page](https://pytorch.org/get-started/locally/#start-locally) regarding the specific install command for your platform to install PyTorch.

When PyTorch has been installed, you can install pandaraller and transformers from source by running:

```linux
pip install pandarallel
git clone https://github.com/huggingface/transformers
cd transformers
pip install .
pip install -r ./examples/requirements.txt
```
When you update the repository, you should upgrade the transformers installation and its dependencies as follows:

```linux
git pull
pip install --upgrade
```
After the transformers have been installed, you can install this project by cloning the repository and running:

```linux
cd ..
git clone https://github.com/Zhen-tam/794_group_project.git
```
Then, you need to replace the processors folder in transformers with the folder with same name in this project,
Importantly, you need to replace the processors folder in the installed transformers directory like this (path are different according to the environment you create in the previous steps, but are simliar. Or you can use `pip list -v` to find where the transformers package is installed):

```linux
sudo rm -r /usr/local/lib/python3.6/dist-packages/transformers/data/processors
sudo mv ./794_group_project/processors/ /usr/local/lib/python3.6/dist-packages/transformers/data/
```
Likewise, you need to replace the metrics folder in transformers with the folder with same name in this project:
```linux
sudo rm -r /usr/local/lib/python3.6/dist-packages/transformers/data/metrics
sudo mv ./794_group_project/metrics/ /usr/local/lib/python3.6/dist-packages/transformers/data/
```
Also, you need to replace the BERT config file in transformers with the file with same name in this project:
```linux
sudo rm -r /usr/local/lib/python3.6/dist-packages/transformers/configuration_bert.py
sudo mv ./794_group_project/configuration_bert.py /usr/local/lib/python3.6/dist-packages/transformers/
```
Then, you need to download the [pre-trained model](https://drive.google.com/drive/folders/1dVrZht7Z9sPAzw31cM4dts_FCHq-Bo7u?usp=sharing), named `mrpc_output`, and save it to some directory `$OUTPUT_DIR`.

Last, you need to download the [GLUE data](https://gluebenchmark.com/tasks) by running the script, `download_glue_data.py`, and unpack it to some directory `$GLUE_DIR`.

## Try the large-scale paraphrasing function
First, for ealuation you need to prepare dataset with specific number of positive examples, n, and number of negative examples, k. I have prepared some [typical dataset](https://drive.google.com/drive/folders/1XENTwJNV_aYgbMLyVV1HEX3l20Yj_BLb?usp=sharing). Their names are in this form: `paraphrase_{n}_{k}.tsv`. Save the folder into a path `$PREPARED_DATA`. And you can choose you target file as `$TARGET_FILE`. If you want, you can produce you own dataset by the notebook `pre-processing.ipynb`, all you need to do is to change the k, n values you want, and file path to your MRPC data in glue_data, very straightforward.

Now, you can run the `just_glue.py` file downloaded like this:
```
export TASK_NAME=MPRC
export GLUE_DIR=/path/to/glue_data
export PREPARED_DATA=/path/to/prepared_data
export TARGET_FILE=/target/filename/in/prepared_data
export OUTPUT_DIR=/path/to/mrpc_output

python just_run.py   --model_type bert   --model_name_or_path $OUTPUT_DIR   --task_name $TASK_NAME   --do_eval   --do_lower_case   --data_dir $GLUE_DIR/$TASK_NAME   --max_seq_length 128   --output_dir $OUTPUT_DIR   --paraphrase_corpus --input_file $PREPARED_DATA/$TARGET_FILE   --overwrite_output_dir   --input_sentence  none
```
Or you can simply input all the path, an example is followed:
```
python just_run.py   --model_type bert   --model_name_or_path  $OUTPUT_DIR   --task_name MRPC   --do_eval   --do_lower_case   --data_dir /home/baipiao_tz/nlp/glue_data/MRPC/   --max_seq_length 128   --output_dir /home/baipiao_tz/nlp/mrpc_output/    --paraphrase_corpus --input_file /home/baipiao_tz/nlp/prepared_data/paraphrase_1_1000.tsv   --overwrite_output_dir   --input_sentence  none
```
### Evaluation and Result
The benchmark result (8 threads at most, with 4 CPU, no GPU, number of entries per example after TF-IDF, M, is 10, number of positive example, N, is 1000) is as following:
| Number of negtive example per entries (K) | recall | tfidf-recall | tfidf-time(s) | total time(s) | total time per example(s) |
| :-------------: | :-------------: | :-------------: | :-------------: | :-------------: | :------------- |
| 10  | 0.9869327390599676  | --- | --- | 633 | 0.063 |
| 50  | 0.9855668036483913  | 1 | 36 | 687 | 0.01374 |
| 100 | 0.9836247852016577| 1 | 73 | 719 | 0.00719 |
| 500 | 0.9738319631040706 | 1 | 441 | 1089 | 0.002178 |
| 1000 | 0.9667797286512371 | 1 | 1046 | 1700 | 0.0017 |

The detailed time consumption analysis for the case when N=1 & k=1000, is as following:
| Total time: 13.3806973916s | step | time (s) |
| :-------------: | :------------- | :------------- | 
| Before eval: 12.5592698079s | Step 1: setting up modes  | 4.777940511703491 |
|   | Step 2: load model  | 3.539000413981012 |
|   | Step 3: remove cache for last testing| 0.021132707595825195 |
|   | Step 4: Corpus Tokenization | 2.3765177726745605 |
|   | Step 5: Tfidf for Corpus S1.1 S.(k-1).1 | 1.8446784019470215 |
| Eval: 0.82142758369s | Step 6: Tokenize S1.2 and Tfidf for S1.2 | 0.0018427371978759766 |
|   | Step 7: compute cosine distance between S1.2 and Corpus | 0.06635570526123047 |
|   | Step 8. Find Argmax 10 | 0.0003757476806640625 |
|   | Step 9: Run BERT on 10 with batch_size=8 | 0.75285339355 |

## References
<a id="1">[1]</a> 
Thomas Wolf, etc. (2019). 
[HuggingFace's Transformers: State-of-the-art Natural Language Processing](https://arxiv.org/pdf/1910.03771.pdf)
ArXiv2019 1910.03771.

<a id="2">[2]</a> 
Jacob Devlin, etc. (2018). 
[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/pdf/1810.04805.pdf)
ArXiv2018 1810.04805.

<a id="3">[3]</a> 
Alex Wang, etc. (2019). 
[GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding](https://arxiv.org/pdf/1804.07461.pdf)
ArXiv2019 1804.07461.

<a id="4">[4]</a> 
Ashish Vaswani, etc. (2017). 
[Attention Is All You Need](https://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf)
NIPS2017 7181.

