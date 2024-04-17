"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import argparse
import pickle
import os
from utils.task_config import task_config
from utils.load_task import load_test_split, format_data
from utils.eval_metrics import evaluate_performance_metric
from utils.response_standardization import standardize_classification_response
from utils.model_completion import get_completion_instance


def get_params():
    """Parse arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection", type=str, required=True, help="task, e.g. arithmetics")
    parser.add_argument("--task", type=str, required=True, help="subtasks, e.g. subtraction")
    parser.add_argument("--instruction_version", type=str, default="en", help="instruction version, e.g. en, or de_from_en")
    parser.add_argument("--model_name", type=str, default="gpt-3.5-turbo-0613", help="model / snapshot")
    parser.add_argument("--temperature", type=float, default=0.2, help="output sampling temperature(between 0 and 2)")
    parser.add_argument("--top_p", type=float, default=1.0, help="nucleus sampling: the model considers the results of "
                                                                 "the tokens with top_p probability mass")
    parser.add_argument("--max_tokens", type=int, default=256, help="maximum number of tokens to generate in a chat "
                                                                    "completion")
    parser.add_argument("--combine_data", default=False, type=bool, help="whether sense generation combined input data,"
                                                                         "only used to specify path")
    parser.add_argument("--path_results", type=str, help="path for storing your results: you need to implement "
                                                         "which/how results are stored in the script")
    parser.add_argument("--path_alternative_sense", default=None, type=str,
                        help="path to generated senses for input data (if not evaluating on original data)")
    parser.add_argument("--language", type=str, default="en", help="language to evaluate on, e.g. en for English,"
                                                                   "this will only be used if no path to an alternative"
                                                                   "sense is provided")
    return parser.parse_args()


def eval_model(
        path_results,
        model_name,
        collection,
        task,
        language,
        instruction_version,
        temperature,
        top_p,
        max_tokens,
        path_alternative_sense
):

    # if translation or paraphrase, load self-generated data
    if path_alternative_sense:
        with open(path_alternative_sense + "dataset.pkl", "rb") as f:
            test_data = pickle.load(f)
        model_input, labels = format_data(test_data, collection, task, instruction_version, model_name)
    else:
        test_data = load_test_split(collection, task, language)
        model_input, labels = format_data(test_data, collection, task, instruction_version, model_name)

    # get completions and responses
    inference_model = get_completion_instance(model_name, temperature, top_p, max_tokens)
    completions, responses = inference_model.get_completions(model_input)

    # standardize / normalize responses and labels, and calculate performance based on these normalized values
    standardization, performance = evaluate_performance_metric(labels, responses)
    print("performance", performance)

    # if task is a classification task, map model responses to categories
    # - this is essentially an analysis step
    if task_config[collection][task]["task_type"] == "classification":

        if collection == "companies" or collection == "writers":
            task = "any"

        answer_to_label = task_config[collection][task]["answer_to_label"][instruction_version]
        predicted_labels = []
        for idx, r in enumerate(standardization["responses"]):
            if idx == 0:
                print("response 0", r)
            # Belebele is multiple choice and uses capitalized letters for answer options.
            if task == "belebele":
                r = r.upper()
            if r in answer_to_label.keys():
                predicted_labels.append(answer_to_label[r])
            elif r[:-1] + "-" + r[-1] in answer_to_label.keys():
                predicted_labels.append(answer_to_label[r[:-1] + "-" + r[-1]])
            elif r.replace(" ", "-") in answer_to_label.keys():
                predicted_labels.append(answer_to_label[r[:-1] + "-" + r[-1]])
            else:
                predicted_labels.append(-1)

        # add evaluation that more generously accepts variations in answer format
        label_map = task_config[collection][task]["answer_to_label"][instruction_version]
        label_map_new = {}
        for key in label_map.keys():
            label_map_new[key.lower()] = label_map[key]
            # the following is for COPA, to accept "option-1", "option 1", and "option1" as correct answers
            label_map_new[key.lower().replace("-", " ")] = label_map[key]
            label_map_new[key.lower().replace("-", "")] = label_map[key]
        # standardize_classification_response is a more elaborate function to map responses to labels
        standardized_response = standardize_classification_response(responses, label_map_new)

        answer_mapped, performance_answer_mapped = evaluate_performance_metric(labels, standardized_response)
        predicted_labels_mapped = [label_map_new[r] if r in label_map_new.keys() else r
                                   for r in answer_mapped["responses"]]

    # You can implement which/how to store model responses, performance, predicted labels etc. here
    # using the path provided through "path_results". In our experiments we stored everything (completions, responses,
    # performance, predicted labels etc. as pickle files. For example:
    with open(path_results + "performance.pkl", "wb") as f:
        pickle.dump(performance, f)


def main():

    args = get_params()
    print(args)

    # test if path already exists
    if not os.path.exists(args.path_results):
        os.makedirs(args.path_results)
    else:
        raise Exception("An experiment with these parameters already exists.")

    # run evaluation
    eval_model(
        args.path_results,
        args.model_name,
        args.collection,
        args.task,
        args.language,
        args.instruction_version,
        args.temperature,
        args.top_p,
        args.max_tokens,
        args.path_alternative_sense
    )


if __name__ == '__main__':
    main()
