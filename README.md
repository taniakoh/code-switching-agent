
# Code Switching Data Translation Pipeline
  <a href="https://huggingface.co/datasets/taniakoh/code-switch-xnli-test">
    <img src="https://img.shields.io/badge/HuggingFace-SwitchLingua_text-yellow?logo=Hugging%20Face" alt="Hugging Face">
  </a>

## Overview
This repo features a data translation pipeline adapted from SwitchLingua. The original use was intended for converting hypotheses from the XNLI dataset into intra-sential code-switched versions for NLI. This repo includes an example of the setup and outputs for 1000 Annotated Sentence Pairs for Intra-Sential Code-Switching Each: English-Spanish(es), English-Vietnamese(vi), English-Mandarin(zh)

## Dataset Structure
#### TSV
```tsv
{"sentence1": original xnli premise,
"sentence2": generated code-switched xnli hypothesis sentence,
"gold_label": classification label(entailment, neutral, contradiction)
}
```

## Environment Setup
### Create a dotenv file
```
API_KEY="YOUR_API_KEY_FOR_LLM"
MODEL="LLM_MODEL" eg. gpt-5-nano
```
## Setup

### 1. Install dependencies

Install all required packages using `npm` based on the dependencies listed in `requirements.txt`:

```sh
npm install
```
### 2. Create config file
#### File Name:
```
config_<language-code>.yaml

```
eg. config_es.yaml

#### Config File Contents:
```
pre_execute:
  cs_ratio:
    - "15%"        # Unused
  use_tools: true
  first_language: "English"
  second_language: "Spanish"   # Change to the full embedding language name
  output_format:
    "json"         # Unused

on_execute:
  round: 1
  verbose: true

```
### 3. Modify agents.py
Open agents.py and update the following variables
#### Language Code
```
code_switch_lang = "es"   # Example: Spanish

```
#### Refiner Iterations
```
max_refiner_iterations = <number>
# Example:
# max_refiner_iterations = 3

```
#### XNLI input row range
```
start = <start_row>
end = <end_row>
# Example:
# start = 0
# end = 200

```
### 4. Run agents.py



## Acknowledgements
All credits for the original Pipeline goes to:

`Xie, P., Liu, X., Chan, T. W., Bie, Y., Song, Y., Wang, Y., Chen, H., & Chen, K. (2025, May 30). SwitchLingua: the first Large-Scale multilingual and Multi-Ethnic Code-Switching dataset. arXiv.org. https://arxiv.org/abs/2506.00087`

All credits for the original XNLI dataset goes to:

`Conneau, Alexis, Ruty Rinott, Guillaume Lample, Adina Williams, Samuel R. Bowman, Holger Schwenk, and Veselin Stoyanov.
"XNLI: Evaluating Cross-lingual Sentence Representations."
Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing.
Association for Computational Linguistics, Brussels, Belgium. 2018.`
