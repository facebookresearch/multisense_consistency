"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import pickle
from datasets import load_dataset, Dataset
from utils.task_config import task_config


def load_test_split(collection, task, language):
    """
    Load test split for a certain task a specific language.
    :param collection: task collection (e.g. "xglue")
    :param task: subtask (e.g. "xnli")
    :param language: langauge (e.g. "en")
    :return: test split in the form of a dataset
    """

    if collection == "arithmetics":
        if task == "addition":
            with open("template_data/addition/dataset_" + language + ".pkl", "rb") as f:
                dataset = pickle.load(f)
        else:
            with open("template_data/addition/dataset_num.pkl", "rb") as f:
                dataset = pickle.load(f)
    elif collection == "elements":
        with open("template_data/elements/dataset.pkl", "rb") as f:
            dataset = pickle.load(f)
        if task == "element_from_position":
            dataset_new = {
                "period": dataset["period"],
                "group": dataset["group"],
                "label": [[elem] for elem in dataset["element"]]
            }
            dataset = Dataset.from_dict(dataset_new)
    elif collection in ["companies", "writers", "olympics"]:
        with open("template_data/" + collection + "/dataset_" + task + ".pkl", "rb") as f:
            dataset = pickle.load(f)
    else:
        if task == "xnli":
            dataset = load_dataset(path="xglue", name=task, split=f"test.{language}",
                                   revision="1cdcf07be24d81f3d782038a5a0b9c8d62f76e60")
        elif task == "paws-x":
            dataset = load_dataset(path=task, name=language, split="test",
                                   revision="8a04d940a42cd40658986fdd8e3da561533a3646")
        elif task == "belebele":
            language_mapping = {"en": "eng_Latn",
                                "de": "deu_Latn",
                                "it": "ita_Latn",
                                "nl": "nld_Latn",
                                "sv": "swe_Latn"}
            dataset = load_dataset(path="facebook/belebele", name=language_mapping[language], split="test",
                                   revision="ac1c539e60eb872d8f4aa5da411c96373530a955")
            dataset = dataset.sort("link")
            dataset = dataset.rename_column("correct_answer_num", "label")
        elif task == "copa":
            if language == "en":
                dataset = load_dataset(path="super_glue", name="copa", split="test",
                                       revision="d05df0885fb0a37b9a05ae5a6cf7084fc2b309c4")
                dataset = dataset.to_dict()
                dataset_for_labels = load_dataset(path="xcopa", name="it", split="test",
                                                  revision="778f59340d3840381b54b40d885b1ac47cdfc2c6")
                dataset["label"] = dataset_for_labels["label"]
                dataset = Dataset.from_dict(dataset)
            else:
                dataset_translation = load_dataset(path="xcopa", name=language, split="test",
                                                   revision="778f59340d3840381b54b40d885b1ac47cdfc2c6")
                dataset = {}
                for column_name in dataset_translation.column_names:
                    if column_name in task_config[collection][task]["column_names"]:
                        dataset[column_name] = dataset_translation[column_name]
                dataset = Dataset.from_dict(dataset)
    return dataset


def format_data(dataset, collection, task, instruction_version, model_name):
    """ Turn test split into model inputs, i.e. combine instruction and input data
    :param dataset: input data, generated with load_task
    :param collection: task collection (e.g., "xglue" or "olympics")
    :param task: actual task ("paws-x", "xnli", etc)
    :param instruction_version: which instruction, e.g. ("it_from_en")
    :param model_name: model snapshot
    """

    if collection == "companies" or collection == "writers":
        task = "any"

    model_inputs = []

    additional_mapping = "additional_mapping" in task_config[collection].keys()

    sentence_keys = task_config[collection][task]["sentence_keys"]

    if instruction_version == "en":
        instruction = task_config[collection][task]["instruction"][instruction_version]
    else:
        instruction = task_config[collection][task]["instruction"][instruction_version][model_name]

    classification = task_config[collection][task]["task_type"] == "classification"

    if classification:
        label_map = task_config[collection][task]["label_to_answer"]

    labels = []
    for datapoint in dataset:

        model_input = instruction
        for i, key in enumerate(sentence_keys):
            model_input = model_input.replace("[" + key.upper() + "]", datapoint[key])
            if additional_mapping:
                mapping = task_config[collection]["additional_mapping"]
                for elem in mapping["keys"]:
                    if collection == "olympics" and "it" in instruction_version:
                        replacement = mapping[instruction_version][elem + "-" + task][datapoint[elem]]
                    else:
                        replacement = mapping[instruction_version][elem][datapoint[elem]]
                    model_input = model_input.replace("[" + elem.upper() + "]", replacement)

        model_inputs.append(model_input)

        if classification:
            labels.append([label_map[instruction_version][datapoint["label"]]])
        else:
            labels.append(datapoint["label"])

    return model_inputs, labels


def combine_dataset(dataset, collection, task, language="en"):
    """Combine input data for en such that it can be translated / paraphrased altogether"""
    model_inputs = []

    sentence_keys = task_config[collection][task]["sentence_keys"]
    template = task_config[collection][task]["combine_data"][language]

    for datapoint in dataset:
        new_datapoint = template
        for key in sentence_keys:
            new_datapoint = new_datapoint.replace("[" + key.upper() + "]", datapoint[key])
        model_inputs.append(new_datapoint)

    new_dataset = {}
    for column_name in dataset.column_names:
        if column_name not in sentence_keys:
            new_dataset[column_name] = dataset[column_name]
    new_dataset["content"] = model_inputs

    combined_dataset = Dataset.from_dict(new_dataset)

    return combined_dataset

