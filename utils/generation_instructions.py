"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""

# We added this file only to show which generation instructions we used for our experiments.
# It is never actually used in the current repository.
# These are the generation instructions that we used for our experiments.
# For details, see also the appendix in our paper.

from utils.translation_config import language_codes

target_language = "x"

generation_instruction = {
    "translate": "Please translate the following text into " + language_codes[target_language] + ":\n",
    "paraphrase": "Please paraphrase the following text:\n",
    "translate-belebele": "Please translate the following text passage, question, and multiple-choice answer "
                          "options (separately) into " + language_codes[target_language] +
                          ". Simply translate everything and do not answer the question.\n\n",
    "paraphrase-xnli": "Please paraphrase the following premise and hypothesis (separately). Reply only with the "
                       "paraphrased text and do not add any additional comments.\n\n",
    "paraphrase-paws-x": "Please paraphrase the following two sentences (separately). Reply only with the "
                         "paraphrased text and do not add any additional comments.\n\n",
    "paraphrase-copa": "Please paraphrase the following premise and two alternatives (separately). Reply only with "
                       "the paraphrased text and do not add any additional comments.\n\n",
    "paraphrase-belebele": "Please paraphrase the following text passage, question, and multiple-choice answer "
                           "options (separately). Make sure to paraphrase everything, including the passage and "
                           "reply only with the paraphrased text and do not add any additional comments.\n\n"
}

# Where instructions were selected in the following manner:

# if prompt_part == "task" and combine_data:
#     if method == "translate" and task == "belebele":
#         instruction = generation_instruction["translate-belebele"]
#     elif method == "paraphrase" and combine_data:
#         instruction = generation_instruction[method + "-" + task]
#     else:
#         instruction = generation_instruction[method]
# else:
#     instruction = generation_instruction[method]
