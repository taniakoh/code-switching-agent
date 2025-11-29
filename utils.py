import yaml
from pprint import pprint
from node_models import AgentRunningState
import jsonlines as jsl
import os
import csv
import json
from read_xnli_dataset import XNLIDataLoader

def load_config(config_path: str):
    # Each config file will generate a different scenarios ~1440
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config

def create_hypo_json():
    # load xnli dataset
    loader = XNLIDataLoader(lang='en', test_path='xnli.test.tsv')
    # get list of hypo
    hypo_list = loader.get_hypotheses_json()
    # save hypo json
    loader.save_to_json("xnli_hypo.json")
    return hypo_list

def load_hypo_json():
    with open("xnli_hypo.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
def generate_hypo_list():
    if os.path.isfile("xnli_hypo.json"):
        hypo_list=load_hypo_json()
    else:
        hypo_list=create_hypo_json()
    return hypo_list
    
def get_premise_label(loader: XNLIDataLoader):
    mapping = {}
    for idx, row in loader.data.iterrows():
        hypo = row['hypo']
        premise = row['premise']
        label = row['label']
        mapping[hypo] = {"premise": premise, "label": label}
    return mapping

def weighting_scheme(state):
    accuracy = state["accuracy_result"]["accuracy_score"]
    fluency = state["fluency_result"]["fluency_score"]
    naturalness = state["naturalness_result"]["naturalness_score"]
    # csratio = state["cs_ratio_result"]["ratio_score"]
    #socio = state["social_cultural_result"]["socio_cultural_score"]
    return accuracy*0.3 + fluency * 0.4 + naturalness * 0.3

def save_jsonl_to_tsv(jsonl_file, tsv_file, loader: XNLIDataLoader):
    """
    Saves code-switched hypotheses from a JSONL file into a TSV ready for XNLI evaluation.
    Uses the XNLIDataLoader to get the original premise and label for each hypothesis.
    """
    entries = []

    # Create a mapping: original hypo -> {premise, label}
    mapping = {row['hypo']: {"premise": row['premise'], "label": row['label']}
               for idx, row in loader.data.iterrows()}

    entries = []
    with jsl.open(jsonl_file, 'r') as reader:
        for obj in reader:
            code_switched_hypo = obj.get("data_translation_result", "")
            original_hypo = obj.get("hypothesis", {}).get("hypo", "")

            if original_hypo in mapping and code_switched_hypo:
                premise = mapping[original_hypo]["premise"]
                label = mapping[original_hypo]["label"]
                translated_sentence = code_switched_hypo.get("translated_sentence", "")
                entries.append({
                    "sentence1": premise,
                    "sentence2": translated_sentence,
                    "gold_label": label
                })


    # Save TSV
    with open(tsv_file, "w", encoding="utf-8", newline="") as tsvfile:
        writer = csv.DictWriter(tsvfile, fieldnames=["sentence1", "sentence2", "gold_label"], delimiter="\t")
        writer.writeheader()
        for row in entries:
            writer.writerow(row)

    print(f"Saved {len(entries)} rows to {tsv_file}")

if __name__ == "__main__":
    if os.path.isfile("xnli_hypo.json"):
        hypo_list=create_hypo_json()
    else:
        hypo_list=load_hypo_json()
    # For a quick peek, let's print the first few
    for i, h in enumerate(hypo_list[:10]):
        print(f"hypo #{i+1}:", h)
        print("\n")
