"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""

# if working with OpenAI models uncomment the following lines and add your organization and api key
# import openai
# openai.organization = ""
# openai.api_key = ""


def get_completion_instance(model_name, temperature, top_p, max_tokens):
    # implement an if condition that returns the correct completion object based on model_name
    # and parameters
    pass


class ModelCompletion:

    def __init__(self, model_name, temperature, top_p, max_tokens):

        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

    def get_completions(self, model_inputs, instruction=None, verbose=True):
        """
        param: model_inputs - list with input datapoints
        param: instruction - will be prepended to each datapoint in model_inputs
        param: verbose - we used this keyword to prompt some example inputs and responses (mainly for debugging)
        returns:    completions, responses
                    completions: list of raw (complete) model completions
                    responses: list of answers to the input extracted from the model completions
        """
        pass


class ExampleModelCompletion(ModelCompletion):
    # this is just an example class showing you what to implement in order to run our simulations with a model
    # of your choice.

    def __init__(self, model_name, temperature, top_p, max_tokens):
        super().__init__(model_name, temperature, top_p, max_tokens)
        # for models that are not accessed through the OpenAI API you can load your model and tokenizer here
        # and add them to the ModelCompletion class as: self.model, self.tokenizer

    def get_completions(self, model_inputs, instruction=None, verbose=True):
        """ see parameters and return statement in ModelCompletion class"""
        # implement your model-specific inference procedure here.

        # for OpenAI model inferences, simply loop over the model input and generate a completion following
        # the instructions here: https://platform.openai.com/docs/guides/text-generation.

        # if you're not working with OpenAI models you can consider batching the inputs here.

        pass





