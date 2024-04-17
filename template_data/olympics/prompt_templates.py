"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
prompt_templates = {
    "hundred_meters": {
        "completion": {
            "en": "The winner of the [MEDAL] medal in the [SEX] 100 meters at the [YEAR] Summer Olympics was ",
            "de": "[WINNER] der [MEDAL]medaille im 100-Meter-Lauf der [SEX] bei den Olympischen Sommerpielen [YEAR] war ",
            "sv": "Vinnaren av [MEDAL]medaljen på [SEX] 100 meter vid de Olympiska sommarspelen [YEAR] var ",
            "lv": "[YEAR]. gada Vasaras Olimpiskajās spēlēs [SEX] 100 metru skrējienā [MEDAL] medaļu [WINNER] bija ",
            "vi": "Người giành huy chương [MEDAL] 100 mét [SEX] tại Thế vận hội Mùa hè [YEAR] là "
        },
        "qa": {
            "en": "Who won the [MEDAL] medal in the [SEX] 100 meters at the [YEAR] Summer Olympics?",
            "de": "Wer gewann die [MEDAL]medaille im 100-Meter-Lauf der [SEX] bei den Olympischen Sommerspielen [YEAR]?",
            "sv": "Vem vann [MEDAL]medaljen på [SEX] 100 meter vid de Olympiska sommarspelen [YEAR]?",
            "lv": "Kas ieguva [MEDAL] medaļu [SEX] 100 metru skrējienā [YEAR]. gada Vasaras Olimpiskajās spēlēs?",
            "vi": "Ai là người giành huy chương [MEDAL] 100 mét [SEX] tại Thế vận hội Mùa hè [YEAR]?"
        }
    },
    "downhill": {
        "completion": {
            "en": "The winner of the [MEDAL] medal in the [SEX] downhill competition at the [YEAR] Winter Olympics was ",
            "de": "[WINNER] der [MEDAL]medaille im Abfahrtsrennen der [SEX] bei den Olympischen Winterspielen [YEAR] war ",
            "sv": "Vinnaren av [MEDAL]medaljen på [SEX] störtlopp vid de Olympiska vinterspelen [YEAR] var ",
            "lv": "[YEAR]. gada Ziemas Olimpiskajās spēlēs [SEX] nobraucienā [MEDAL] medaļu [WINNER] bija ",
            "vi": "Người giành huy chương [MEDAL] trượt tuyết đổ đèo [SEX] tại Thế vận hội mùa đông [YEAR] là "
        },
        "qa": {
            "en": "Who won the [MEDAL] medal in the [SEX] downhill competition at the [YEAR] Winter Olympics?",
            "de": "Wer gewann die [MEDAL]medaille im Abfahrtsrennen der [SEX] bei den Olympischen Winterspielen [YEAR]?",
            "sv": "Vem vann [MEDAL]medaljen på [SEX] störtlopp vid de Olympiska vinterspelen [YEAR]?",
            "lv": "Kas ieguva [MEDAL] medaļu [SEX] nobraucienā [YEAR]. gada Ziemas Olimpiskajās spēlēs?",
            "vi": "Ai là người giành huy chương [MEDAL] trượt tuyết đổ đèo [SEX] tại Thế vận hội mùa đông [YEAR]?"
        }
    }
}

medal_templates = {
    "en": {"gold": "gold", "silver": "silver", "bronze": "bronze"},
    "de": {"gold": "Gold", "silver": "Silber", "bronze": "Bronze"},
    "sv": {"gold": "guld", "silver": "silver", "bronze": "brons"},
    "lv": {"gold": "zelta", "silver": "sudraba", "bronze": "bronzas"},
    "vi": {"gold": "vàng", "silver":"bạc", "bronze": "đồng"}
}

sex_templates = {
    "en": {"m": "men's", "f": "women's"},
    "de": {"m": "Männer", "f": "Frauen"},
    "sv": {"m": "herrarnas", "f": "damernas"},
    "lv": {"m": "vīriešu", "f": "sieviešu"},
    "vi": {"m": "nam", "f": "nữ"}
}

winner_templates = {
    "de": {"f": "Die Gewinnerin", "m": "Der Gewinner"},
    "lv": {"f": "ieguvēja", "m": "ieguvējs"}
}


####################################################################


prompt_templates_gpt_turbo_0613 = {
    "hundred_meters": {
        "qa": {
            "en_from_de": "Who won the [MEDAL] medal in the [SEX] 100-meter race at the [YEAR] Summer Olympics?",
            "en_from_sv": "Who won the [MEDAL] medal in the [SEX] 100 meters at the [YEAR] Olympic Summer Games?",
            "de_from_en": "Wer gewann die [MEDAL]medaille im 100-Meter-Lauf der [SEX] bei den Olympischen Sommerspielen [YEAR]?",   # SAME
            "sv_from_en": "Vem vann [MEDAL]medaljen i [SEX] 100 meter vid sommar-OS [YEAR?"
        }
    },
    "downhill": {
        "qa": {
            "en_from_de": "Who won the [MEDAL] medal in the [SEX] downhill race at the [YEAR] Winter Olympic Games?",
            "en_from_sv": "Who won the [MEDAL] medal in the [SEX] downhill at the [YEAR] Winter Olympics?",
            "de_from_en": "Wer hat die [MEDAL]medaille im [SEX]-Abfahrtsrennen bei den Olympischen Winterspielen [YEAR] gewonnen?",
            "sv_from_en": "Vem vann [MEDAL]medaljen i [SEX] störtloppstävling vid vinter-OS [YEAR]?"
        }
    }
}

medal_templates_gpt_turbo_0613 = {
    "en_from_de": {"gold": "gold", "silver": "silver", "bronze": "bronze"},
    "en_from_sv": {"gold": "gold", "silver": "silver", "bronze": "bronze"},
    "de_from_en": {"gold": "Gold", "silver": "Silber", "bronze": "Bronze"},
    "sv_from_en": {"gold": "guld", "silver": "silver", "bronze": "brons"}
}

sex_templates_gpt_turbo_0613 = {
    "hundred_meters": {
        "en_from_de": {"m": "men's", "f": "women's"},
        "en_from_sv": {"m": "men's", "f": "women's"},
        "de_from_en": {"m": "Männer", "f": "Frauen"},
        "sv_from_en": {"m": "herrarnas", "f": "damernas"}
    },
    "downhill": {
        "en_from_de": {"m": "men's", "f": "women's"},
        "en_from_sv": {"m": "men's", "f": "women's"},
        "de_from_en": {"m": "Herren", "f": "Damen"},
        "sv_from_en": {"m": "herrarnas", "f": "damernas"}
    }
}





