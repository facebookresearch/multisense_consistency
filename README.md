# From Form(s) to Meaning

## Table of Contents

- [Overview](#Overview)
  - [Citation](#Citation)
- [Datasets](#Datasets)
- [Models](#Models)
- [Consistency evaluation](#Consistency-evaluation)
  - [Sense generation](#1-Sense-generation)
  - [Model evaluation (on the task)](#2-Model-evaluation-on-the-task)
  - [Consistency calculation](#3-Consistency-calculation)
- [Our results and analyses](#Our-results-and-analyses)
- [Contact](#Contact)


## Overview

This repository provides code for evaluating the self-consistency of LLMs across different forms of the same task.
Our evaluation is based on the principle that the same underlying meaning can often be articulated through different linguistic expressions, each representing distinct senses of that meaning.
Given a task, we ask the model under investigation to generate an alternative form of that task (through paraphrasing or translation), and then evaluate the consistency between the model's responses to these two task versions. 
If the model has a meaning-based, rather than a form-based task understanding, its responses should be consistent.

### Citation
Aside from serving as a starting point for new multisense consistency experiments, the repository contains datasets, results, and analyses for the experiments in the following paper:

> ***Xenia Ohmer, Elia Bruni, and Dieuwke Hupkes. "From Form(s) to Meaning: Probing the Semantic Depths of Language Models Using Multisense Consistency".***

Please cite this paper if you use any of the materials we provide here. 


## Datasets

The code is generalizable to various QA and classification-style tasks. 
To add a specific dataset, you have to:
1. Add the task configuration including the original English instruction to *utils/task_config.py*, in analogy to the other task configurations. 
2. Configure how your dataset is loaded in *utils/load_task.py* (load_test_split).

In addition, we release some template-based datasets for testing simple factual knowledge, that we also use in our paper.
They can be found in the folder *template_data/*.
There is a subfolder for each task, containing the csv files with the data as well as a notebook to convert the csv files into datasets.
The datasets include facts about [addition](template_data/addition), [company headquarters locations](template_data/companies), [atomic numbers of chemical elements](template_data/elements), [names of olympic medalists](template_data/olympics), and [birth years of known writers](template_data/writers).
You can also use the code to evaluate models on the benchmark datasets that we use in our experiments, which will be downloaded on the fly.


## Models 

To use this repository to evaluate multisense consistency for a specific model, you have to implement a class that handles generating outputs for a given set of inputs for this model.
All model-specific aspects are implemented in *utils/model_completion.py*.
Simply derive a class from ModelCompletion that takes care of the inference step for your model. 
For instance, to evaluate an OpenAI model, add in your OpenAI API key and credentials, and implement a class that generates a model completion via the API.

Specifically, to add a model:
1. Add your ModelCompletion class to *utils/model_completion.py* (see the ExampleModelCompletion class).
2. Add a line of code for loading the correct inference model in *get_completion_instance* (in the same file) based on the model_name provided to *eval.py* or *generate_senses.py*.


## Consistency evaluation

Evaluating multisense consistency consists of three main steps: 1) generating an alternative sense,  2) evaluating the model on both the original and the alternative sense, 
and 3) evaluating the model's consistency based on its responses to both task versions.
In the following, we describe these three steps in more detail. 

### 1. Sense generation
The different senses (translations and paraphrases) of the tasks are generated with *generate_senses.py*.
You can run generate_senses for both the task instruction (*--prompt_part instruction*) and the input data (*--prompt_part task*). 
The prompts for generating translations or paraphrases can also be modified in this file, and you can find our prompts in our paper as well as in *utils/generation_instructions.py*.
Once you have translated or paraphrased the task instruction, add it to *utils/task_config.py*.

When generating an alternative sense of the input data, you can choose two different options. 
Either, you combine all elements of a given datapoint (for example _sentence1_ and _sentence2_ in paraphrase identification) and translate/paraphrase them jointly. 
Or, you can translate/paraphrase each of these elements separately, resulting in more inferences.
You can choose between these options using *--combine_data True* or *--combine_data False*, respectively.
If you choose to evaluate jointly, you need to specify how the datapoint components should be combined when they are being passed to the model in *utils/task_config.py*.
Combining the entries for each datapoint has the advantage that paraphrases / translations of the dataset entries belonging to that datapoint will be consistent. 
However, in that case, you need to recompose a dataset from the model outputs that matches the column structure of the original dataset. 
We found that joint generation leads to slightly better performance on the generated senses, and report these results in the paper. 
For examples of how we recomposed the datasets, see *standardize_translation.ipynb*.

**Examples**

To generate a translation of the elements-from-position template (see our paper for details on that dataset) from English to Swedish, run
```
python generate_senses.py --collection elements --task number_from_position --source_language en --target_language sv --prompt_part instruction --method translate
```
To paraphrase the input data of Belebele, run
```
python generate_senses.py --collection individual --task belebele --source_language en --target_language en --prompt_part task --method paraphrase
```

Setting the flag *--combine_data* is only relevant when working with the benchmark data (not the simple facts), and when generating an alternative sense for the input data (*--prompt_part task*).


### 2. Model evaluation (on the task)
The model can be evaluated on the original task and the alternative senses (generated in step 1) with *eval.py*.
Note that if you want to evaluate on alternative senses, these senses need to be generated first.

When you run an evaluation on an existing (original) dataset, you need to provide the language that you want to use with "--language" and the appropriate language code (e.g. en, de, sv, nl, etc.).
Else, if you want to evaluate on a dataset (alternative sense) that was generated by the model, specify the path to this dataset with "--path_alternative_sense".
The instruction that you want to use must exist in your task configuration. 

In our experiments, we label these instructions "en" (original English), "en-paraphrase" (English paraphrase), and "de_from_en" (translation from English to German), etc.

**Examples**

If you evaluate the model in the template datasets, alternative senses are only generated for the template.
The datapoints can be plugged in without any translations since they consist of names or years.
Hence, you should always select "--language en" and specify the language via the instruction.
E.g., to evaluate the model on the olympics-downhill dataset with a paraphrased version of the task (template), run:
```
python eval.py --collection olympics --task downhill --language en --instruction en-paraphrase
```
Arithmetics is the only simple facts dataset that requires translating the input data, too. 
Here, we translated the two numbers separately, using the flag *--combine_data False* during sense generation.
To evaluate the model on the arithmetics dataset with a translation of the task (i.e. template and numbers) from English to Dutch, run:
```
python eval.py --collection arithmetics --task addition --instruction nl_from_en --path_alternative_sense (your path to the translated_numbers)
```
On the benchmark data, you can combine different senses for the input data and/or instruction.
E.g., to evaluate the model on XNLI with the original English input data but a translation of the instruction to German, run:
```
python eval.py --collection xglue --task xnli --language en --instruction de_from_en
```
Or, to evaluate the model on the complete translation of PAWS-X (input data and instruction) from English to Swedish, run:
```
python eval.py --collection individual --task paws-x --instruction sv_from_en --path_alternative_sense (your path to the translated input data)
```


### 3. Consistency calculation
Whether two answers are consistent (i.e. whether they have the same meaning) can be determined in different ways.
For example, the consistency for classification-type tasks can be determined by mapping the model's responses to the corresponding class labels - for the original and the alternative sense - and then calculating the overlap between these predictions.
The mapping process from model response to class label is handled automatically in *eval.py* based on the response-label mappings that you provide in *utils/task_config* for your dataset. 
The consistency calculation can then be handled in your analysis file.

In our experiments, we choose the implementations you can find in *analysis_utils/load_scores.py*.
1) Template data: We evaluate consistency for the template datasets based on whether the two responses refer to the same entity.
The datasets provide a set of possible correct answers for each datapoint, which accounts for variations in naming (e.g. “Charles Paddock”, “Charlie Paddock”, “Charles William Paddock”),
including variations between the languages that we use (e.g. “Berlin”, “Berlino”, “Berlijn”).
We say that two model responses are consistent if they fall into the same set of possible answers.
2) Benchmark data: The benchmark datasets are classification-type tasks. Thus, we extract the predicted labels from the model's responses and calculate the percentage of overlapping predictions. 



## Our results and analyses

In *results/* you can find the performance scores for our experiments with GPT-3.5-turbo.
For classification tasks, the folder also contains the model's answers after mapping them to the set of possible answers as well as the corresponding predicted labels.
E.g. for PAWS-en, the mapped answers consist of "yes" and "no", and the predicted labels of "0" and "1".
If you would like to get access to the model's translations, paraphrases, or the raw model responses from our evaluations, please contact us.

All our analyses and plots for the simple facts data and the benchmark data can be found in the notebooks *analyze_simple_facts.ipynb* and *analyze_benchmark_data.ipynb*, respectively.

## Contact

Do not hesitate to reach out to xenia.ohmer@uni-osnabrueck.de if you have any questions. 

## License
Please see the license file for information about usage.
