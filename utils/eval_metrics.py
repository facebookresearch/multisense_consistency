"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import string
import pickle
import evaluate
from collections import Counter
from comet import download_model, load_from_checkpoint
from template_data.addition.arithmetics_utils import alternative_formulation


def normalize_answer(s):
    """Lower text and remove punctuation and extra whitespace."""

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        basic_punctuation = list(string.punctuation)
        other_punctuation = ["！", "？", "｡", "。", "＂", "＃", "＄", "％", "＆", "＇", "（", "）", "＊", "＋", "，",
                             "－", "／", "：", "；", "＜", "＝", "＞", "＠", "［", "＼", "］", "＾", "＿", "｀", "｛",
                             "｜", "｝", "～", "｟", "｠", "｢", "｣", "、", "〃", "》", "「", "」", "『", "』", "【",
                             "】", "〔", "〕", "〖", "〗", "〘", "〙", "〚", "〛", "〜", "〝", "〞", "〟", "〰", "–", "—",
                             "‘", "’", "‛", "“", "”", "„", "‟", "…", "‧", "﹏", ".", "。"]
        exclude = set(basic_punctuation + other_punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_punc(lower(s)))


def f1_score(prediction, ground_truth):
    """Calculate F1 score for answer"""

    prediction_tokens = prediction.split()
    ground_truth_tokens = ground_truth.split()

    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)

    return f1


def exact_match_score(prediction, ground_truth):
    """Calculate exact match score for answer"""
    return prediction == ground_truth


def contained_score(prediction, ground_truth):
    """Calculate containment score: is correct answer in the model's response."""
    return ground_truth in prediction


def metric_max_over_ground_truths(metric_fn, prediction, ground_truths):
    """Evaluate for every possible correct answer in answer set, choose the highest possible score."""
    scores_for_ground_truths = []
    for ground_truth in ground_truths:
        score = metric_fn(prediction, ground_truth)
        scores_for_ground_truths.append(score)
    return max(scores_for_ground_truths)


def evaluate_answers(labels, predictions):
    """Given labels and predictions, calculate various performance metrics."""
    f1 = exact_match = contained = total = exact_match_no_blanks = contained_no_blanks = 0

    for i in range(len(labels)):
        exact_match += metric_max_over_ground_truths(exact_match_score, predictions[i], labels[i])
        f1 += metric_max_over_ground_truths(f1_score, predictions[i], labels[i])
        contained += metric_max_over_ground_truths(contained_score, predictions[i], labels[i])
        total += 1

    exact_match = 100.0 * exact_match / total
    f1 = 100.0 * f1 / total
    contained = 100.0 * contained / total

    return {'exact_match': exact_match,
            'f1': f1,
            'contained': contained}


def evaluate_performance_metric(labels, responses):
    """Normalize answers and evaluate performance."""
    standardized = {}

    standardized_responses = [normalize_answer(r) for r in responses]
    standardized_labels = []

    for i in range(len(labels)):
        standardized_labels.append([normalize_answer(l) for l in labels[i]])

    result = evaluate_answers(standardized_labels, standardized_responses)

    standardized["responses"] = standardized_responses
    standardized["labels"] = standardized_labels

    return standardized, result


def evaluate_number_match(path_translation, language, dataset_size=500):
    """Evaluate whether the model's translations of spelled-out numbers are correct."""
    path_data = "template_data/addition/"
    correct_number1 = []
    correct_number2 = []
    correct_both = []

    keys = ["number1", "number2"]

    with open(path_data + "dataset_" + language + ".pkl", "rb") as f:
        data_target_orig = pickle.load(f)
    with open(path_translation + "dataset.pkl", "rb") as f:
        data_mt = pickle.load(f)

    n = len(data_mt["number1"])

    data_target = {"number1": [], "number2": []}

    for i in range(n):
        for key in ["number1", "number2"]:
            dp_orig = data_target_orig[key][i]
            data_target[key].append([dp_orig] + alternative_formulation(language, dp_orig))

    key1, key2 = keys
    for i in range(dataset_size):
        r1 = normalize_answer(data_mt[key1][i]).replace(" ", "")
        r2 = [normalize_answer(data_target[key1][i][j]).replace(" ", "") for j in range(len(data_target[key1][i]))]
        r3 = normalize_answer(data_mt[key2][i]).replace(" ", "")
        r4 = [normalize_answer(data_target[key2][i][j]).replace(" ", "") for j in range(len(data_target[key2][i]))]
        correct_number1.append(int(r1 in r2))
        correct_number2.append(int(r3 in r4))
        correct_both.append(int((r1 in r2) and (r3 in r4)))

    correct_translation = {
        "mean_both": sum(correct_both)/len(correct_both),
        "mean_number1": sum(correct_number1)/len(correct_number1),
        "mean_number2": sum(correct_number2)/len(correct_number2),
    }

    for i in range(n):
        if not correct_number2[i]:
            print(data_mt["number2"][i], data_target["number2"][i])

    return correct_translation


def evaluate_translation_quality(
        sentence_keys,
        source_data,
        target_data,
        translation_data,
        combine_components=False
):
    """Calculate metrics for translation quality, based on source data, translations, and reference data."""

    sources = []
    machine_translations = []
    references = []

    if not combine_components:
        for key in sentence_keys:
            sources += source_data[key]
            machine_translations += translation_data[key]
            references += target_data[key]
    else:
        for i in range(len(source_data[sentence_keys[0]])):
            src_tmp = ""
            mt_tmp = ""
            ref_tmp = ""
            for key in sentence_keys:
                src_tmp += source_data[key][i].strip(" .") + ". "
                mt_tmp += translation_data[key][i].strip(" .") + ". "
                ref_tmp += target_data[key][i].strip(" .") + ". "
            sources.append(src_tmp.strip(" "))
            machine_translations.append(mt_tmp.strip(" "))
            references.append(ref_tmp.strip(" "))
            if i < 3:
                print(src_tmp, "\n", mt_tmp, "\n", ref_tmp)

    n = len(sources)

    eval_data = []
    for i in range(n):
        if not machine_translations[i] == "NA":
            eval_data.append(
                {
                    "src": sources[i],
                    "mt": machine_translations[i],
                    "ref": references[i]
                }
            )

    print("translation eval data: ", eval_data[0])
    print("length translation eval data: ", len(eval_data))

    model_path = download_model("Unbabel/wmt22-comet-da")
    model = load_from_checkpoint(model_path)
    comet_scores = model.predict(eval_data, batch_size=8, gpus=0)

    bleu = evaluate.load("sacrebleu")
    tokenize = "13a"
    bleu_scores = bleu.compute(predictions=machine_translations,
                               references=[[ref] for ref in references],
                               tokenize=tokenize)

    rouge = evaluate.load("rouge")
    rouge_scores = rouge.compute(predictions=machine_translations, references=references)
    rouge_1 = rouge_scores["rouge1"]
    rouge_2 = rouge_scores["rouge2"]
    rouge_l = rouge_scores["rougeL"]

    results = {
        "comet": comet_scores[-1],
        "bleu": bleu_scores["score"],
        "rouge1": rouge_1,
        "rouge2": rouge_2,
        "rouge-l": rouge_l,
        "comet_all": comet_scores,
        "bleu_all": bleu_scores,
        "rouge_all": rouge_scores
    }

    return results
