"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import pickle
import re
import pandas as pd
from analysis_utils.mappings import name_mappings, city_mappings
from utils.load_task import load_test_split

collection_task_all = {
    
    "facts": [
        ("arithmetics", "addition"),
        ("elements", "number_from_element"),
        ("elements", "number_from_position"),
        ("olympics", "hundred_meters"),
        ("olympics", "downhill"),
        ("writers", "english"),
        ("writers", "german"),
        ("writers", "italian"),
        ("writers", "dutch"),
        ("writers", "swedish"),
        ("companies", "us"),
        ("companies", "de"),
        ("companies", "it"),
        ("companies", "nl"),
        ("companies", "sv")
    ],
    
    "benchmarks": [
        ("individual", "paws-x"), 
        ("xglue", "xnli"), 
        ("superglue", "copa"), 
        ("individual", "belebele")
    ]
    
}


def accuracy_facts(languages=("en", "en-paraphrase", "de_from_en", "it_from_en", "nl_from_en", "sv_from_en")):
    
    collection_task = collection_task_all["facts"]    
    performance_scores = dict.fromkeys([elem1 + "_" + elem2 for elem1, elem2 in collection_task])
    exact_match = dict.fromkeys([elem1 + "_" + elem2 for elem1, elem2 in collection_task])
    containment_score = dict.fromkeys([elem1 + "_" + elem2 for elem1, elem2 in collection_task])
    for key in performance_scores.keys():
        performance_scores[key] = {}
        exact_match[key] = {}
        containment_score[key] = {}

    for collection, task in collection_task:
        for language in languages:
            
            if collection == "arithmetics":
                if "paraphrase" in language: 
                    language_path = language.split("-")[0] + "/" + language + "/"
                elif language == "en_2nd_run":
                    language_path = language + "/" + "en/"
                else:
                    language_path = language + "/" + language + "/"
            else:
                language_path = "en/" + language + "/"
                
            path = ("results/" + collection + "_" + task + "/temp-0.2_topp-1.0_maxt-256/" + language_path)
            try:
                with open(path + "performance.pkl", "rb") as f:
                    performance = pickle.load(f)
            except:
                continue
            performance_scores[collection + "_" + task][language] = performance
            exact_match[collection + "_" + task][language] = round(performance["exact_match"], 2)
    return performance_scores, exact_match


def consistency_facts(get_details=False):
    
    collection_task = collection_task_all["facts"]
    
    languages = ["en_2nd_run", "en-paraphrase", "de_from_en", "it_from_en", "nl_from_en", "sv_from_en"]
    consistency = dict.fromkeys([elem1 + "_" + elem2 for elem1, elem2 in collection_task])
    correct_responses_src = dict.fromkeys([elem1 + "_" + elem2 for elem1, elem2 in collection_task])
    correct_responses_target = dict.fromkeys([elem1 + "_" + elem2 for elem1, elem2 in collection_task])
    all_consistencies = dict.fromkeys([elem1 + "_" + elem2 for elem1, elem2 in collection_task])
    for key in consistency.keys():
        consistency[key] = {}
        correct_responses_src[key] = {}
        correct_responses_target[key] = {}
        all_consistencies[key] = {}

    for collection, task in collection_task:

        path = ("results/" + collection + "_" + task + "/temp-0.2_topp-1.0_maxt-256/LANGUAGE/INSTRUCTION/")
        path_src = path.replace("LANGUAGE", "en").replace("INSTRUCTION", "en")

        with open(path_src + "standardization.pkl", "rb") as f:
            standardized = pickle.load(f)
        responses_src = standardized["responses"]
        labels_src = standardized["labels"]
        n = len(labels_src)

        for language in languages:
                       
            if task == "addition":
                if "paraphrase" in language:
                    path_target = path.replace("LANGUAGE", language.split("-")[0]).replace("INSTRUCTION", language)
                elif "en_2nd_run" in language:
                    path_target = path.replace("LANGUAGE", language).replace("INSTRUCTION", "en")
                else:
                    path_target = path.replace("LANGUAGE", language).replace("INSTRUCTION", language)
            else:
                path_target = path.replace("LANGUAGE", "en").replace("INSTRUCTION", language)
            
            with open(path_target + "standardization.pkl", "rb") as f:
                standardized = pickle.load(f)
            responses_tgt = standardized["responses"]
            labels_tgt = standardized["labels"]
            
            if collection == "arithmetics": 
                responses_src = [re.sub("[^0-9]", "", r) for r in responses_src]
                responses_tgt = [re.sub("[^0-9]", "", r) for r in responses_tgt]
            if collection == "companies":
                responses_src = [city_mappings[r] if r in city_mappings.keys() else r for r in responses_src]
                responses_tgt = [city_mappings[r] if r in city_mappings.keys() else r for r in responses_tgt]
            if collection == "olympics":
                responses_src = [name_mappings[r] if r in name_mappings.keys() else r for r in responses_src]
                responses_tgt = [name_mappings[r] if r in name_mappings.keys() else r for r in responses_tgt]
            
            consistency[collection + "_" + task][language] = round(sum(
                [responses_src[i] == responses_tgt[i] for i in range(n)]
            ) *100 / n, 2)
            
            if get_details:
                all_consistencies[collection + "_" + task][language] = [responses_src[i] == responses_tgt[i] 
                                                                        for i in range(n)]
                correct_responses_src[collection + "_" + task][language] = [r in labels_src[i] 
                                                                            for i, r in enumerate(responses_src)]
                correct_responses_target[collection + "_" + task][language] = [r in labels_tgt[i] 
                                                                               for i, r in enumerate(responses_tgt)]
    if get_details:
        return consistency, all_consistencies, correct_responses_src, correct_responses_target
    else:
        return consistency


def accuracy_benchmarks(combine=True, response_mapping=False, ablation=None, external=False):
    
    collection_task = collection_task_all["benchmarks"]
    
    if external:
        languages = ["de", "it", "nl", "sv"]
    else:
        languages = ["en", "en-paraphrase", "de_from_en", "it_from_en", "nl_from_en", "sv_from_en"]
    performance_scores = {"paws-x": {}, "xnli": {}, "copa": {}, "belebele": {}}
    exact_match = {"paws-x": {}, "xnli": {}, "copa": {}, "belebele": {}}

    for collection, task in collection_task:
        
        for language in languages:
            
            instruction = language
            load_language = language
            if external:
                instruction = language + "_from_en"
            if ablation == "instruction": 
                instruction = "en"
            if ablation == "task":
                load_language = "en"
            if combine:
                instruction = instruction + "-combined"

            path_results = ("results/" + collection + "_" + task + "/temp-0.2_topp-1.0_maxt-256/" +
                            load_language + "/" + instruction + "/")
            try:
                if response_mapping:
                    with open(path_results + "performance_answer_mapped.pkl", "rb") as f:
                        performance = pickle.load(f)
                else:
                    with open(path_results + "performance.pkl", "rb") as f:
                        performance = pickle.load(f)
            except: 
                continue
            performance_scores[task][language] = performance
            exact_match[task][language] = round(performance["exact_match"], 2)
    return performance_scores, exact_match


def accuracy_benchmarks_second_run(response_mapping=True):
    
    collection_task = collection_task_all["benchmarks"]
    
    load_language = "en"
    instruction = "en_2nd_run"

    performance_scores = {"paws-x": {}, "xnli": {}, "copa": {}, "belebele": {}}
    exact_match = {"paws-x": {}, "xnli": {}, "copa": {}, "belebele": {}}

    for collection, task in collection_task:
        
        path_results = ("results/" + collection + "_" + task + "/temp-0.2_topp-1.0_maxt-256/" +
                        load_language + "/" + instruction + "/")
        if response_mapping:
            with open(path_results + "performance_answer_mapped.pkl", "rb") as f:
                performance = pickle.load(f)
        else:
            with open(path_results + "performance.pkl", "rb") as f:
                performance = pickle.load(f)

        performance_scores[task]["en_2nd_run"] = performance
        exact_match[task]["en_2nd_run"] = round(performance["exact_match"], 2)
        
    return performance_scores, exact_match


def translation_scores(combine=True, references=True, joint_eval=True):
    
    languages = ["de_from_en", "it_from_en", "nl_from_en", "sv_from_en"]
    translation_scores = {"addition": {}, "paws-x": {}, "xnli": {}, "copa": {}, "belebele": {}}
    bleu = {"paws-x": {}, "xnli": {}, "copa": {}, "belebele": {}}
    number_match = {"addition": {}}

    for collection, task in (
        ("arithmetics", "addition"),
        ("individual", "paws-x"),
        ("xglue", "xnli"),
        ("superglue", "copa"),
        ("individual", "belebele")
    ):
        
        if task == "addition":
            combine_data = False
        elif not combine:
            combine_data = False
        else:
            combine_data = True
            
        if references:
            if joint_eval:
                load_name = "translation_scores_combined.pkl"
            else:
                load_name = "translation_scores.pkl"
        else:
            load_name = "translation_scores_no_reference.pkl"
        
        for language in languages:
            path_translations = ("translations/task/" + collection + "_" + task +
                                 "/temp-0.2_topp-1.0_maxt-2048/combined_" + str(combine_data) + "/" + language + "/")
            if task == "addition" and references: 
                with open(path_translations + "number_match.pkl", "rb") as f:
                    translation_performance = pickle.load(f)
                number_match[task][language] = translation_performance["mean_both"]
            else:
                try:
                    with open(path_translations + load_name, "rb") as f:
                        translation_performance = pickle.load(f)
                    if "bleu" in translation_performance.keys():
                        bleu[task][language] = translation_performance["bleu"]
                        translation_performance.pop("comet_all")
                    else:
                        translation_performance = translation_performance["system_score"]
                except:
                    continue
            translation_scores[task][language] = translation_performance
            
    return translation_scores, bleu, number_match


def consistency_benchmarks(combine=True, response_mapping=False, external=False, ablation=None, get_details=False):
    
    collection_task = collection_task_all["benchmarks"]
    
    if external: 
        languages = ["de", "it", "nl", "sv"]
    else:
        languages = ["en", "en-paraphrase", "de_from_en", "it_from_en", "nl_from_en", "sv_from_en"]
    consistency = {"paws-x": {}, "xnli": {}, "copa": {}, "belebele": {}}
    
    if get_details:
        correct_responses_src = dict.fromkeys([elem2 for elem1, elem2 in collection_task])
        correct_responses_target = dict.fromkeys([elem2 for elem1, elem2 in collection_task])
        all_consistencies = dict.fromkeys([elem2 for elem1, elem2 in collection_task])
        for key in consistency.keys():
            correct_responses_src[key] = {}
            correct_responses_target[key] = {}
            all_consistencies[key] = {}

    for collection, task in collection_task:

        path = "results/" + collection + "_" + task + "/temp-0.2_topp-1.0_maxt-256/LANGUAGE/INSTRUCTION/"
        path_src = path.replace("LANGUAGE", "en").replace("INSTRUCTION", "en")
        append = "_answer_mapped.pkl" if response_mapping else ".pkl"
        
        if get_details:
            gt_labels = load_test_split(collection, task, "en")["label"]
        
        with open(path_src + "predicted_labels" + append, "rb") as f:
            labels_src = pickle.load(f)
        n = len(labels_src)
        
        for language in languages:
            
            instruction = language
            load_language = language
            if external:
                instruction = language + "_from_en"
            if ablation == "instruction": 
                instruction = "en"
            if ablation == "task":
                load_language = "en"
            if combine:
                instruction = instruction + "-combined"
            if language == "en":
                load_language = "en"
                instruction = "en_2nd_run"
                
            path_target = path.replace("LANGUAGE", load_language).replace("INSTRUCTION", instruction)
            
            try:
                with open(path_target + "predicted_labels" + append, "rb") as f:
                    labels_target = pickle.load(f)
            except:
                continue

            m = 0
            wrong_format = 0
            labels1 = []
            labels2 = []
            for i in range(n):
                if labels_src[i] == -1 or labels_target[i] == -1:
                    wrong_format += 1
                if labels_src[i] != -1 or labels_target[i] != -1:
                    m += 1
                    labels1.append(labels_src[i])
                    labels2.append(labels_target[i])                
            
            consistency[task][language] = sum([labels1[i] == labels2[i] for i in range(m)]) * 100 / m
            
            if wrong_format > 0:
                print(collection, task, language, "wrong format:", wrong_format/n)
            
            if get_details:
                all_consistencies[task][language] = [labels_src[i] == labels_target[i] for i in range(n)]
                correct_responses_src[task][language] = [labels_src[i] == gt_labels[i] for i in range(n)]
                correct_responses_target[task][language] = [labels_target[i] == gt_labels[i] for i in range(n)]
                
    if get_details:
        return consistency, all_consistencies, correct_responses_src, correct_responses_target
    else:
        return consistency


def make_aggregate_df_from_table(table, score="accuracy"):
    df = {"task": [], "language": [], score: []}

    table_df = pd.DataFrame(table)
    companies_df = table_df[["companies_us", "companies_de", "companies_it", "companies_nl", "companies_sv"]]
    writers_df = table_df[["writers_english", "writers_german", "writers_italian", "writers_dutch", "writers_swedish"]]

    companies_flag = False
    writers_flag = False
    for task in table.keys():
        if task.split("_")[0] != "companies" and task.split("_")[0] != "writers":
            for language in table[task].keys():
                df["task"].append(task)
                df["language"].append(language)
                df[score].append(table[task][language])
        else:
            if task.split("_")[0] == "companies" and not companies_flag:
                for language in table[task].keys():
                    df["task"].append(task.split("_")[0])
                    df["language"].append(language)
                    df[score].append(companies_df.aggregate("mean", axis=1)[language])
                companies_flag = True
            elif task.split("_")[0] == "writers" and not writers_flag:
                for language in table[task].keys():
                    df["task"].append(task.split("_")[0])
                    df["language"].append(language)
                    df[score].append(writers_df.aggregate("mean", axis=1)[language])
                writers_flag = True
    return pd.DataFrame(df)


def make_df_from_table(table, score="accuracy"):
    df = {"task": [], "language": [], score: []}

    for task in table.keys():
        for language in table[task].keys():
            df["task"].append(task)
            df["language"].append(language)
            df[score].append(table[task][language])

    return pd.DataFrame(df)


def fully_consistent(acc1, acc2):
    return 100 - abs(acc1-acc2)
