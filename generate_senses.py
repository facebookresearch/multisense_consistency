"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import argparse
import pickle
import os
from datasets import Dataset
from utils import load_task
from utils.response_standardization import cut_double_quotes
from utils.task_config import task_config
from utils.translation_config import language_codes
from utils.eval_metrics import evaluate_translation_quality, evaluate_number_match
from utils.model_completion import get_completion_instance


def get_params():
    """Parse arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_new_dataset", type=str, default="generated_senses/", help="directory for storing the"
                                                                                          "generated dataset")
    parser.add_argument("--collection", type=str, required=True, help="xglue, or individual_tasks")
    parser.add_argument("--task", type=str, required=True, help="subtask, e.g. xnli")
    parser.add_argument("--target_language", type=str, help="target language")
    parser.add_argument("--source_language", type=str, default="en")
    parser.add_argument("--prompt_part", type=str, required=True, help="instruction or task")
    parser.add_argument("--temperature", type=float, default=0.2, help="output sampling temperature (between 0 and 2)")
    parser.add_argument("--top_p", type=float, default=1.0, help="nucleus sampling: top_p probability mass")
    parser.add_argument("--max_tokens", type=int, default=2048, help="maximum number of tokens to generate")
    parser.add_argument("--method", type=str, default="translate", help="either translate, paraphrase, or improve")
    parser.add_argument("--combine_data", type=bool, default=True, help="whether to translate dataset columns "
                                                                         "separately or combined")
    return parser.parse_args()


def generate(
        path,
        model_name,
        collection,
        task,
        method,
        combine_data,
        source_language,
        target_language,
        prompt_part,
        temperature,
        top_p,
        max_tokens,
):

    # these are very basic default instructions
    # change or extend this to your liking
    # for details on our instructions, see the appendix in our paper or "utils/our_generation_instructions.py"
    generation_instruction = {
        "translate": "Please translate the following text into " + language_codes[target_language] + ":\n",
        "paraphrase": "Please paraphrase the following text:\n",
    }

    instruction = generation_instruction[method]

    inference_model = get_completion_instance(model_name, temperature, top_p, max_tokens)

    # generate alternative sense for instruction: copy-paste the generated instruction to utils/task_config afterward
    if prompt_part == "instruction":

        text = task_config[collection][task]["instruction"][source_language]
        completions, responses = inference_model.get_completions([text], instruction=instruction)

        # store model response (and completions if you like)
        # with open(path + "completions.pkl", "wb") as f:
        #     pickle.dump(completions[0], f)
        with open(path + "response.pkl", "wb") as f:
            pickle.dump(responses[0], f)

    # generate alternative sense for input data
    elif prompt_part == "task":

        test_data = load_task.load_test_split(collection, task, source_language)
        if combine_data:
            test_data = load_task.combine_dataset(test_data, collection, task)
        alternative_data = {}
        completions = {}

        for column_name in test_data.column_names:
            if column_name in task_config[collection][task]["sentence_keys"] or column_name == "content":
                print("Generating " + column_name)

                completions_sentence_key, responses_tmp = inference_model.get_completions(
                    test_data[column_name],
                    instruction=instruction
                )
                responses_sentence_key = [cut_double_quotes(r).strip(": \n") for r in responses_tmp]

                completions[column_name] = completions_sentence_key
                alternative_data[column_name] = responses_sentence_key
            else:
                print("Keeping " + column_name)
                alternative_data[column_name] = test_data[column_name]

        ds_alternative = Dataset.from_dict(alternative_data)

        # store generated dataset (and completions if you like)
        # with open(path + "completions.pkl", "wb") as f:
        #     pickle.dump(completions, f)
        with open(path + "dataset.pkl", "wb") as f:
            pickle.dump(ds_alternative, f)

        # if sense is generated through translation, evaluate translation quality if possible
        # this is an analysis step and you can remove it
        if method == "translate" and task_config[collection][task]["multilingual"]:

            # for the addition task, we need a particular evaluation method, using the ground truth
            # spelled out numbers in other languages (see also template_data/addition/arithmetics_utils.py)
            if task == "addition":
                number_match = evaluate_number_match(path, target_language)
                print("number match", number_match)
                with open(path + "number_match.pkl", "wb") as f:
                    pickle.dump(number_match, f)
            else:
                ground_truth_exists = target_language in task_config[collection][task]["languages"]
                if ground_truth_exists and not combine_data:
                    from utils.load_task import load_test_split
                    translation_quality_metrics = evaluate_translation_quality(
                        task_config[collection][task]["sentence_keys"],
                        test_data,  # source
                        load_test_split(collection, task, target_language),  # target
                        alternative_data  # translation
                    )

                    # store the translation scores
                    with open(path + "translation_scores.pkl", "wb") as f:
                        pickle.dump(translation_quality_metrics, f)


def main():
    args = get_params()
    print(args)

    if not os.path.exists(args.path_new_dataset):
        os.makedirs(args.path_new_dataset)
    else:
        raise Exception("An experiment with these parameters already exists.")

    # generate senses
    generate(
        args.path_new_dataset,
        args.model_name,
        args.collection,
        args.task,
        args.method,
        args.combine_data,
        args.source_language,
        args.target_language,
        args.prompt_part,
        args.temperature,
        args.top_p,
        args.max_tokens
    )


if __name__ == '__main__':
    main()
