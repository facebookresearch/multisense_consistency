"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
prompt_templates = {
        "completion": {
            "en": "The capital of [COUNTRY] is ",
            "de": "Die Hauptstadt von [COUNTRY] ist ",
            "sv": "Huvudstaden i [COUNTRY] är ",
            "lv": "[COUNTRY]s galvaspilsēta ir ",
            "vi": "Thủ đô của [COUNTRY] là "
        },
        "qa": {
            "en": "What is the capital of [COUNTRY]?",
            "de": "Was ist die Hauptstadt von [COUNTRY]?",
            "sv": "Vad är huvudstaden i [COUNTRY]?",
            "lv": "Kas ir [COUNTRY]s galvaspilsēta?",
            "vi": "Thủ đô của [COUNTRY] là gì?"
        }
}

prompt_templates_gpt_turbo_0613 = {
    "qa": {
        "en_from_de": "What is the capital of [COUNTRY]?",      # SAME
        "en_from_sv": "What is the capital of [COUNTRY]?",      # SAME
        "sv_from_en": "Vad är huvudstaden i [COUNTRY]?",        # SAME
        "de_from_en": "Was ist die Hauptstadt von [COUNTRY]?"   # SAME
    }
}
