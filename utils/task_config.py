"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""

task_config = {

    "consistency": {

        "addition": {
            "instruction": "Consider the following two numbers, written out in different languages:\n"
                           "Number 1: [RESPONSE1]\n"
                           "Number 2: [RESPONSE2]\n"
                           "Do these two numbers express the same value? "
                           "Please answer with a single word, either \"yes\" or \"no\"."
        }

    },


    "olympics": {

        "additional_mapping": {
            "keys": ["sex", "medal"],
            "en": {
                "sex": {"m": "men's", "f": "women's"},
                "medal": {"gold": "gold", "silver": "silver", "bronze": "bronze"}
            },
            "en-paraphrase": {
                "sex": {"m": "men's", "f": "women's"},
                "medal": {"gold": "gold", "silver": "silver", "bronze": "bronze"}
            },
            "de_from_en": {
                "sex": {"m": "Herren", "f": "Damen"},
                "medal": {"gold": "Gold", "silver": "Silber", "bronze": "Bronze"}
            },
            "sv_from_en": {
                "sex": {"m": "herrarnas", "f": "damernas"},
                "medal": {"gold": "guld", "silver": "silver", "bronze": "brons"}
            },
            "it_from_en": {
                "sex-hundred_meters": {"m": "maschili", "f": "femminili"},
                "sex-downhill": {"m": "maschile", "f": "femminile"},
                "medal-hundred_meters": {"gold": "d'oro", "silver": "d'argento", "bronze": "di bronzo"},
                "medal-downhill": {"gold": "d'oro", "silver": "d'argento", "bronze": "di bronzo"}
            },
            "nl_from_en": {
                "sex": {"m": "mannen", "f": "vrouwen"},
                "medal": {"gold": "gouden", "silver": "zilveren", "bronze": "bronzen"}
            }
        },

        "hundred_meters": {
            "task_type": "qa",
            "column_names": ("year", "medal", "sex", "label"),
            "sentence_keys": ["year"],
            "multilingual": False,
            "languages": ["en"],
            "instruction": {
                "en": "Who won the [MEDAL] medal in the [SEX] 100 meters at the [YEAR] Summer Olympics? Please"
                      " reply with the name only and do not use any additional words.",
                "en-paraphrase": {
                    "gpt-3.5-turbo-0613": "Please provide the name of the athlete who won the [MEDAL] medal in the "
                                          "[SEX] 100 meters at the [YEAR] Summer Olympics, using only the name and no "
                                          "extra words."
                },
                "de_from_en": {
                    "gpt-3.5-turbo-0613": "Wer hat die [MEDAL]-Medaille im [SEX]-100-Meter-Lauf bei den Olympischen "
                                          "Sommerspielen [YEAR] gewonnen? Bitte antworten Sie nur mit dem Namen und "
                                          "verwenden Sie keine zusätzlichen Wörter."
                },
                "sv_from_en": {
                    "gpt-3.5-turbo-0613": "Vem vann [MEDAL] medaljen i [SEX] 100 meter vid sommar-OS [YEAR]? "
                                          "Vänligen svara med namnet endast och använd inga ytterligare ord."
                },
                "nl_from_en": {
                    "gpt-3.5-turbo-0613": "Wie heeft de [MEDAL] medaille gewonnen op de 100 meter voor [SEX] "
                                          "tijdens de Zomerspelen van [YEAR]? Antwoord alstublieft alleen met de "
                                          "naam en gebruik geen extra woorden."
                },
                "it_from_en": {
                    "gpt-3.5-turbo-0613": "Chi ha vinto la medaglia [MEDAL] nei 100 metri [SEX] alle Olimpiadi "
                                          "estive del [YEAR]? Si prega di rispondere solo con il nome e di non "
                                          "utilizzare altre parole aggiuntive."
                }
            }
        },

        "downhill": {
            "task_type": "qa",
            "column_names": ("year", "medal", "sex", "label"),
            "sentence_keys": ["year"],
            "multilingual": False,
            "languages": ["en"],
            "instruction": {
                "en": "Who won the [MEDAL] medal in the [SEX] downhill competition at the [YEAR] Winter Olympics? "
                      "Please reply with the name only and do not use any additional words.",
                "en-paraphrase": {
                    "gpt-3.5-turbo-0613": "Please provide the name of the athlete who won the [MEDAL] medal in the "
                                          "[SEX] downhill competition at the [YEAR] Winter Olympics, "
                                          "without using any extra words."
                },
                "de_from_en": {
                    "gpt-3.5-turbo-0613": "Wer hat die [MEDAL]-Medaille im [SEX]-Abfahrtsrennen bei den Olympischen"
                                          " Winterspielen [YEAR] gewonnen? Bitte anworten Sie nur mit dem Namen und "
                                          "verwenden Sie keine zusätzlichen Wörter."
                },
                "sv_from_en": {
                    "gpt-3.5-turbo-0613": "Vem vann [MEDAL] medaljen i [SEX] störtloppstävling vid vinter-OS [YEAR]? "
                                          "Vänligen svara med namnet endast och använd inga ytterligare ord."
                },
                "nl_from_en": {
                    "gpt-3.5-turbo-0613": "Wie heeft de [MEDAL] medaille gewonnen in de [SEX] afdaling wedstrijd "
                                          "op de [YEAR] Olympische Winterspelen? Antwoord alstublieft alleen met de "
                                          "naam en gebruik geen extra woorden."
                },
                "it_from_en": {
                    "gpt-3.5-turbo-0613": "Chi ha vinto la medaglia [MEDAL] nella gara di discesa libera [SEX] "
                                          "alle Olimpiadi invernali del [YEAR]? Per favore, rispondi solo con il nome "
                                          "e non utilizzare altre parole aggiuntive."
                }
            }
        }
    },

    "elements": {

        "element_from_position": {
            "task_type": "qa",
            "column_names": ("period", "group", "element", "label"),
            "sentence_keys": ("period", "group"),
            "multilingual": False,
            "languages": ["en"],
            "instruction": {
                "en": "What element is in period [PERIOD] and group [GROUP]? Please provide only the element's symbol"
                      "and do not use any additional words in your response."
            }
        },

        "number_from_element": {
            "task_type": "qa",
            "column_names": ("period", "group", "element", "label"),
            "sentence_keys": ["element"],
            "multilingual": False,
            "languages": ["en"],
            "instruction": {
                "en": "What is the atomic number of the chemical element [ELEMENT]? Please reply with the number only "
                      "and do not use any additional words.",
                "en-paraphrase": {
                    "gpt-3.5-turbo-0613": "Please provide the atomic number of the chemical element [ELEMENT] using "
                                          "only the number and no extra words."
                },
                "de_from_en": {
                    "gpt-3.5-turbo-0613": "Was ist die Ordnungszahl des chemischen Elements [ELEMENT]? Bitte "
                                          "antworten Sie nur mit der Zahl und verwenden Sie keine zusätzlichen Wörter."
                },
                "sv_from_en": {
                    "gpt-3.5-turbo-0613": "Vad är det atomnummer för grundämnet [ELEMENT]. Vänligen svara endast med "
                                          "numret och använd inga ytterligare ord."
                },
                "nl_from_en": {
                    "gpt-3.5-turbo-0613": "Wat is het atoomnummer van het chemisch element [ELEMENT]. Antwoord "
                                          "alstublieft alleen met het nummer en gebruik geen extra woorden."
                },
                "it_from_en": {
                    "gpt-3.5-turbo-0613": "Qual è il numero atomico dell'elemento chimico [ELEMENT]. Si prega di "
                                          "rispondere solo con il numero e di non utilizzare altre parole aggiuntive."
                }
            }
        },

        "number_from_position": {
            "task_type": "qa",
            "column_names": ("period", "group", "element", "label"),
            "sentence_keys": ("period", "group"),
            "multilingual": False,
            "languages": ["en"],
            "instruction": {
                "en": "What is the atomic number of the chemical element in period [PERIOD] and group [GROUP]? Please "
                      "reply with the number only and do not use any additional words.",
                "en-paraphrase": {
                    "gpt-3.5-turbo-0613": "Please provide the atomic number of the element in period [PERIOD] and group"
                                          " [GROUP]. Respond with only the number and no extra words.",
                },
                "de_from_en": {
                    "gpt-3.5-turbo-0613": "Was ist die Ordnungszahl des chemischen Elements in Periode [PERIOD] und "
                                          "Gruppe [GROUP]. Bitte antworten Sie nur mit der Zahl und verwenden Sie "
                                          "keine zusätzlichen Wörter."
                },
                "sv_from_en": {
                    "gpt-3.5-turbo-0613": "Vad är det atomnummer för det kemiska elementet i period [PERIOD] och grupp "
                                          "[GROUP]. Vänligen svara endast med numret och använd inga ytterligare ord.",
                },
                "nl_from_en": {
                    "gpt-3.5-turbo-0613": "Wat is het atoomnummer van het chemisch element in periode [PERIOD] en "
                                          "groep [GROUP]. Antwoord alstublieft alleen met het nummer en gebruik geen "
                                          "extra woorden."
                },
                "it_from_en": {
                    "gpt-3.5-turbo-0613": "Qual è il numero atomico dell'elemento chimico nel periodo [PERIOD] e nel "
                                          "gruppo [GROUP]. Si prega di rispondere solo con il numero e di non "
                                          "utilizzare altre parole aggiuntive."
                }
            }
        }
    },

    "companies": {

        "any": {
            "task_type": "qa",
            "column_names": ("company", "label"),
            "sentence_keys": ["company"],
            "multilingual": False,
            "languages": ["en"],
            "instruction": {
                "en": "In what city does [COMPANY] have its headquarters? Please reply only with the name of the city "
                      "and no additional words.",
                "en-paraphrase": {
                    "gpt-3.5-turbo-0613": "Where is the headquarters of [COMPANY] located? Please respond with only "
                                          "the city name, without any extra words."
                },
                "de_from_en": {
                    "gpt-3.5-turbo-0613": "In welcher Stadt hat [COMPANY] seinen Hauptsitz? Bitte antworten Sie nur "
                                          "mit dem Namen der Stadt und ohne zusätzliche Wörter."
                },
                "sv_from_en": {
                    "gpt-3.5-turbo-0613": "I vilken stad har [COMPANY] sitt huvudkontor? Vänligen svara endast med "
                                          "stadens namn och inga ytterligare ord."
                },
                "nl_from_en": {
                    "gpt-3.5-turbo-0613": "In welke stad heeft [COMPANY] zijn hoofdkantoor? Antwoord alstublieft "
                                          "alleen met de naam van de stad en geen extra woorden."
                },
                "it_from_en": {
                    "gpt-3.5-turbo-0613": "In quale città ha sede [COMPANY]? Si prega di rispondere solo con il nome "
                                          "della città e senza parole aggiuntive."
                }
            }
        }

    },

    "writers": {

        "any": {
            "task_type": "qa",
            "column_names": ("author", "label"),
            "sentence_keys": ["author"],
            "multilingual": False,
            "languages": ["en"],
            "instruction": {

                "en": "In what year was the writer [AUTHOR] born? Please reply with the correct year only and do not "
                      "use any additional words.",

                "en-paraphrase": {
                    "gpt-3.5-turbo-0613": "What is the birth year of the author [AUTHOR]? Please respond with only the"
                                          " correct year and avoid using extra words."
                },
                "de_from_en": {
                    "gpt-3.5-turbo-0613": "In welchem Jahr wurde der Schriftsteller / die Schriftstellerin [AUTHOR] "
                                          "geboren? Bitte antworten Sie nur mit dem korrekten Jahr und verwenden Sie "
                                          "keine zusätzlichen Wörter."
                },
                "sv_from_en": {
                    "gpt-3.5-turbo-0613": "I vilket år föddes författaren [AUTHOR]? Ditt svar ska bara bestå av det "
                                          "korrekta året."
                },
                "nl_from_en": {
                    "gpt-3.5-turbo-0613": "In welk jaar is de schrijver [AUTHOR] geboren? Uw antwoord moet alleen "
                                          "bestaan uit het juiste jaartal."
                },
                "it_from_en": {
                    "gpt-3.5-turbo-0613": "In che anno è nato lo scrittore / è nata la scrittrice [AUTHOR]? Per "
                                          "favore, rispondi solo con l'anno corretto e non utilizzare altre parole "
                                          "aggiuntive."
                }
            }
        }

    },

    "arithmetics": {

        "addition-numerical": {
            "task_type": "qa",
            "column_names": ("number1", "number2", "label"),
            "sentence_keys": ("number1", "number2"),
            "multilingual": False,
            "languages": ["en"],
            "instruction": {
                "en": "What is [NUMBER1] plus [NUMBER2]? Please reply with only the correct number "
                      "(in numerical form) and no additional words.",
                "en-paraphrase": {
                    "gpt-3.5-turbo-0613": "What is the sum of [NUMBER1] and [NUMBER2]? Please respond with only "
                                          "the correct numerical answer and no extra words."
                },
                "de_from_en": {
                    "gpt-3.5-turbo-0613": "Was ist [NUMBER1] plus [NUMBER2]? Bitte antworten Sie nur mit der korrekten "
                                          "Zahl (in numerischer Form) und ohne zusätzliche Wörter."
                },
                "sv_from_en": {
                    "gpt-3.5-turbo-0613": "Vad är [NUMBER1] plus [NUMBER2]? Vänligen svara endast med det korrekta "
                                          "numret (i numerisk form) och inga ytterligare ord."
                },
                "nl_from_en": {
                    "gpt-3.5-turbo-0613": "Wat is [NUMBER1] plus [NUMBER2]? Antwoord alstublieft alleen met het juiste "
                                          "nummer (in numerieke vorm) en geen extra woorden."
                },
                "it_from_en": {
                    "gpt-3.5-turbo-0613": "Quanto fa [NUMBER1] più [NUMBER2]? Si prega di rispondere solo con il "
                                          "numero corretto (in forma numerica) e senza parole aggiuntive."
                }
            }
        },

        "addition": {
            "task_type": "qa",
            "column_names": ("number1", "number2", "label"),
            "sentence_keys": ("number1", "number2"),
            "multilingual": True,
            "languages": ["en", "de", "sv", "nl", "it"],
            "instruction": {
                "en": "What is [NUMBER1] plus [NUMBER2]? Please reply with only the correct number "
                      "(in numerical form) and no additional words.",
                "en-paraphrase": {
                    "gpt-3.5-turbo-0613": "What is the sum of [NUMBER1] and [NUMBER2]? Please respond with only "
                                          "the correct numerical answer and no extra words."
                },
                "de_from_en": {
                    "gpt-3.5-turbo-0613": "Was ist [NUMBER1] plus [NUMBER2]? Bitte antworten Sie nur mit der korrekten "
                                          "Zahl (in numerischer Form) und ohne zusätzliche Wörter."
                },
                "sv_from_en": {
                    "gpt-3.5-turbo-0613": "Vad är [NUMBER1] plus [NUMBER2]? Vänligen svara endast med det korrekta "
                                          "numret (i numerisk form) och inga ytterligare ord."
                },
                "nl_from_en": {
                    "gpt-3.5-turbo-0613": "Wat is [NUMBER1] plus [NUMBER2]? Antwoord alstublieft alleen met het juiste "
                                          "nummer (in numerieke vorm) en geen extra woorden."
                },
                "it_from_en": {
                    "gpt-3.5-turbo-0613": "Quanto fa [NUMBER1] più [NUMBER2]? Si prega di rispondere solo con il "
                                          "numero corretto (in forma numerica) e senza parole aggiuntive."
                }
            }
        }

    },


    "superglue": {

        "copa": {
            "task_type": "classification",
            "column_names": ("premise", "choice1", "choice2", "question", "idx", "label"),
            "sentence_keys": ("premise", "choice1", "choice2"),
            "n_labels": 2,
            "multilingual": True,
            "languages": ["et", "id", "it", "qu", "th"],
            "label_to_answer": {
                "en": {0: "alternative-1", 1: "alternative-2"},
                "en-paraphrase": {0: "option-1", 1: "option-2"},
                "de_from_en": {0: "alternative-1", 1: "alternative-2"},
                "nl_from_en": {0: "alternatief-1", 1: "alternatief-2"},
                "it_from_en": {0: "alternativa-1", 1: "alternativa-2"},
                "sv_from_en": {0: "alternativ-1", 1: "alternativ-2"}
            },
            "answer_to_label": {
                "en": {"alternative-1": 0, "alternative-2": 1},
                "en-paraphrase": {"option-1": 0, "option-2": 1},
                "de_from_en": {"alternative-1": 0, "alternative-2": 1},
                "nl_from_en": {"alternatief-1": 0, "alternatief-2": 1},
                "it_from_en": {"alternativa-1": 0, "alternativa-2": 1},
                "sv_from_en": {"alternativ-1": 0, "alternativ-2": 1}
            },
            "combine_data": {
                "en": "Premise: \"[PREMISE]\"\nAlternative 1: \"[CHOICE1]\"\nAlternative 2: \"[CHOICE2]\"",
                "de": "Prämisse: \"[PREMISE]\"\nAlternative 1: \"[CHOICE1]\"\nAlternative 2: \"[CHOICE2]\"",
                "nl": "Premisse: \"[PREMISE]\"\nAlternatief 1: \"[CHOICE1]\"\nAlternatief 2: \"[CHOICE2]\"",
                "it": "Presupposto: \"[PREMISE]\"\nAlternativa 1: \"[CHOICE1]\"\nAlternativa 2: \"[CHOICE2]\"",
                "sv": "Premiss: \"[PREMISE]\"\nAlternativ 1: \"[CHOICE1]\"\nAlternativ 2: \"[CHOICE2]\""
            },
            "instruction": {
                "en": "Given the following premise, which of the two alternatives is more plausible?\n"
                      "Premise: \"[PREMISE]\"\n"
                      "Alternative 1: \"[CHOICE1]\"\n"
                      "Alternative 2: \"[CHOICE2]\"\n"
                      "Please answer with a single word: \"Alternative-1\" if alternative 1 is more plausible and "
                      "\"Alternative-2\" if alternative 2 is more plausible.",
                "en-paraphrase": {
                    "gpt-3.5-turbo-0613": "Based on the provided premise, which of the two options is more likely?\n"
                                          "Premise: \"[PREMISE]\"\n"
                                          "Option 1: \"[CHOICE1]\"\n"
                                          "Option 2: \"[CHOICE2]\"\n"
                                          "Please respond with either \"Option-1\" if option 1 is more likely, or "
                                          "\"Option-2\" if option 2 is more likely."
                },
                "de_from_en": {
                    "gpt-3.5-turbo-0613": "Angesichts der folgenden Prämisse, welche der beiden Alternativen ist "
                                          "plausibler?\n"
                                          "Prämisse: \"[PREMISE]\"\n"
                                          "Alternative 1: \"[CHOICE1]\"\n"
                                          "Alternative 2: \"[CHOICE2]\"\n"
                                          "Bitte antworten Sie mit einem einzigen Wort: \"Alternative-1\", wenn "
                                          "Alternative 1 plausibler ist, und \"Alternative-2\", wenn Alternative 2 "
                                          "plausibler ist."
                },
                "nl_from_en": {
                    "gpt-3.5-turbo-0613": "Gegeven de volgende premisse, welke van de twee alternatieven is "
                                          "waarschijnlijker?\n"
                                          "Premisse: \"[PREMISE]\"\n"
                                          "Alternatief 1: \"[CHOICE1]\"\n"
                                          "Alternatief 2: \"[CHOICE2]\"\n"
                                          "Antwoord alstublieft met één woord: \"Alternatief-1\" als alternatief 1 "
                                          "waarschijnlijker is en \"Alternatief-2\" als alternatief 2 waarschijnlijker "
                                          "is."
                },
                "it_from_en": {
                    "gpt-3.5-turbo-0613": "Dato il seguente presupposto, quale delle due alternative è più "
                                          "plausibile?\n"
                                          "Presupposto: \"[PREMISE]\"\n"
                                          "Alternativa 1: \"[CHOICE1]\"\n"
                                          "Alternativa 2: \"[CHOICE2]\"\n"
                                          "Per favore, rispondi con una sola parola: \"Alternativa-1\" se "
                                          "l'alternativa 1 è più plausibile e \"Alternativa-2\" se l'alternativa 2 è "
                                          "più plausibile."
                },
                "sv_from_en": {
                    "gpt-3.5-turbo-0613": "Givet följande premiss, vilket av de två alternativen är mer troligt?\n"
                                          "Premiss: \"[PREMISE]\"\n"
                                          "Alternativ 1: \"[CHOICE1]\"\n"
                                          "Alternativ 2: \"[CHOICE2]\"\n"
                                          "Svara med ett enda ord: \"Alternativ-1\" om alternativ 1 är mer troligt och "
                                          "\"Alternativ-2\" om alternativ 2 är mer troligt."
                },
            }
        }

    },

    "xglue": {

        "xnli": {

            "task_type": "classification",

            "column_names": ("premise", "hypothesis", "label"),

            "sentence_keys": ("premise", "hypothesis"),

            "n_labels": 3,

            "multilingual": True,

            "languages": ["ar", "bg", "de", "el", "en", "es", "fr", "hi", "ru", "sw", "th", "tr", "ur", "vi", "zh"],

            "instruction": {
                "en": "Given the following premise and hypothesis, please identify whether the premise entails "
                      "the hypothesis, contradicts the hypothesis, or neither of the two.\n"
                      "Premise: \"[PREMISE]\"\n"
                      "Hypothesis: \"[HYPOTHESIS]\"\n"
                      "Please reply with a single word: \"entailment\" if the premise entails the hypothesis, "
                      "\"contradiction\" if the premise contradicts the hypothesis, and \"neutral\" if the premise "
                      "neither entails nor contradicts the hypothesis.",
                "en-paraphrase": {
                    "gpt-3.5-turbo-0613": "Please determine if the premise and hypothesis are related.\n"
                                          "Premise: \"[PREMISE]\"\n"
                                          "Hypothesis: \"[HYPOTHESIS]\"\n"
                                          "If the premise supports the hypothesis, indicate \"entailment\". If the "
                                          "premise contradicts the hypothesis, indicate \"contradiction\". If there is "
                                          "no clear relationship between the two, indicate \"neutral\"."
                },
                "de_from_en": {
                    "gpt-3.5-turbo-0613": "Angesichts der folgenden Prämisse und Hypothese, bitte identifizieren Sie, "
                                          "ob die Prämisse die Hypothese impliziert, der Hypothese widerspricht oder "
                                          "weder das eine noch das andere.\n"
                                          "Prämisse: \"[PREMISE]\"\n"
                                          "Hypothese: \"[HYPOTHESIS]\"\n"
                                          "Bitte antworten Sie mit einem einzigen Wort: \"Implikation\", wenn die "
                                          "Prämisse die Hypothese impliziert, \"Widerspruch\", wenn die Prämisse der "
                                          "Hypothese widerspricht, und \"neutral\", wenn die Prämisse weder die "
                                          "Hypothese impliziert noch ihr widerspricht."
                },
                "nl_from_en": {
                    "gpt-3.5-turbo-0613": "Gegeven de volgende premisse en hypothese, identificeer alstublieft of de "
                                          "premisse de hypothese impliceert, de hypothese tegenspreekt, "
                                          "of geen van beide.\n"
                                          "Premisse: \"[PREMISE]\"\n"
                                          "Hypothese: \"[HYPOTHESIS]\"\n"
                                          "Antwoord alstublieft met één woord: \"implicatie\" als de premisse de "
                                          "hypothese impliceert, \"tegenspraak\" als de premisse de hypothese "
                                          "tegenspreekt, en \"neutraal\" als de premisse noch de hypothese impliceert "
                                          "noch tegenspreekt."
                },
                "sv_from_en": {
                    "gpt-3.5-turbo-0613": "Givet följande premiss och hypotes, vänligen ange om premissen innebär "
                                          "hypotesen, motsäger hypotesen eller varken innebär eller motsäger "
                                          "hypotesen.\n"
                                          "Premiss: \"[PREMISE]\"\n"
                                          "Hypotes: \"[HYPOTHESIS]\"\n"
                                          "Vänligen svara med ett enda ord: \"innebär\" om premissen innebär "
                                          "hypotesen, \"motsäger\" om premissen motsäger hypotesen och \"neutral\" "
                                          "om premissen varken innebär eller motsäger hypotesen."
                },
                "it_from_en": {
                    "gpt-3.5-turbo-0613": "Dato il seguente presupposto e ipotesi, per favore identifica se il "
                                          "presupposto implica l'ipotesi, contraddice l'ipotesi o né implica né "
                                          "contraddice l'ipotesi.\n"
                                          "Presupposto: \"[PREMISE]\"\n"
                                          "Ipotesi: \"[HYPOTHESIS]\"\n"
                                          "Per favore rispondi con una sola parola: \"implicazione\" se il presupposto "
                                          "implica l'ipotesi, \"contraddizione\" se il presupposto contraddice "
                                          "l'ipotesi e \"neutrale\" se il presupposto né implica né contraddice "
                                          "l'ipotesi."
                },
            },

            "combine_data": {
                "en": "Premise: \"[PREMISE]\"\nHypothesis: \"[HYPOTHESIS]\"",
                "de": "Prämisse: \"[PREMISE]\"\nHypothese: \"[HYPOTHESIS]\"",
                "sv": "Premiss: \"[PREMISE]\"\nHypotes: \"[HYPOTHESIS]\"",
                "nl": "Premisse: \"[PREMISE]\"\nHypothese: \"[HYPOTHESIS]\"",
                "it": "Presupposto: \"[PREMISE]\"\nIpotesi: \"[HYPOTHESIS]\""
            },

            "answer_to_label": {
                "en": {"entailment": 0, "neutral": 1, "contradiction": 2},
                "en-paraphrase": {"entailment": 0, "neutral": 1, "contradiction": 2},
                "de_from_en": {"implikation": 0, "neutral": 1, "widerspruch": 2},
                "nl_from_en": {"implicatie": 0, "neutraal": 1, "tegenspraak": 2},
                "sv_from_en": {"innebär": 0, "neutral": 1, "motsäger": 2},
                "it_from_en": {"implicazione": 0, "neutrale": 1, "contraddizione": 2}
            },

            "label_to_answer": {
                "en": {0: "entailment", 1: "neutral", 2: "contradiction"},
                "en-paraphrase": {0: "entailment", 1: "neutral", 2: "contradiction"},
                "de_from_en": {0: "implikation", 1: "neutral", 2: "widerspruch"},
                "nl_from_en": {0: "implicatie", 1: "neutraal", 2: "tegenspraak"},
                "sv_from_en": {0: "innebär", 1: "neutral", 2: "motsäger"},
                "it_from_en": {0: "implicazione", 1: "neutrale", 2: "contraddizione"}
            }
        },

    },

    "individual": {

        "belebele": {

            "task_type": "classification",

            "column_names": ('link', 'question_number', 'flores_passage', 'question', 'mc_answer1', 'mc_answer2',
                             'mc_answer3', 'mc_answer4', 'label', 'dialect', 'ds'),

            "sentence_keys": ("flores_passage", "question", "mc_answer1", "mc_answer2", "mc_answer3", "mc_answer4"),

            "multilingual": True,

            "languages": ["en", "de", "sv", "nl", "it"],

            "answer_to_label": {
                "en": {"A": "1", "B": "2", "C": "3", "D": "4"},
                "en-paraphrase": {"A": "1", "B": "2", "C": "3", "D": "4"},
                "de_from_en": {"A": "1", "B": "2", "C": "3", "D": "4"},
                "nl_from_en": {"A": "1", "B": "2", "C": "3", "D": "4"},
                "sv_from_en": {"A": "1", "B": "2", "C": "3", "D": "4"},
                "it_from_en": {"A": "1", "B": "2", "C": "3", "D": "4"},
            },

            "label_to_answer": {
                "en": {"1": "A", "2": "B", "3": "C", "4": "D"},
                "en-paraphrase": {"1": "A", "2": "B", "3": "C", "4": "D"},
                "de_from_en": {"1": "A", "2": "B", "3": "C", "4": "D"},
                "nl_from_en": {"1": "A", "2": "B", "3": "C", "4": "D"},
                "sv_from_en": {"1": "A", "2": "B", "3": "C", "4": "D"},
                "it_from_en": {"1": "A", "2": "B", "3": "C", "4": "D"},
            },

            "combine_data": {
                "en": "[FLORES_PASSAGE]\n\n"
                      "[QUESTION]\n\n"
                      "Option A: [MC_ANSWER1]\n"
                      "Option B: [MC_ANSWER2]\n"
                      "Option C: [MC_ANSWER3]\n"
                      "Option D: [MC_ANSWER4]\n",
            },

            "instruction": {
                "en": "[FLORES_PASSAGE]\n\n"
                      "[QUESTION]\n\n"
                      "Option A: [MC_ANSWER1]\n"
                      "Option B: [MC_ANSWER2]\n"
                      "Option C: [MC_ANSWER3]\n"
                      "Option D: [MC_ANSWER4]\n\n"
                      "Please reply with \"A\", \"B\", \"C\", or \"D\" to indicate the correct answer. "
                      "Your reply should be a single letter and should not contain any additional words.",
                "en-paraphrase": {
                    "gpt-3.5-turbo-0613": "[FLORES_PASSAGE]\n\n"
                                          "[QUESTION]\n\n"
                                          "A) [MC_ANSWER1]\n"
                                          "B) [MC_ANSWER2]\n"
                                          "C) [MC_ANSWER3]\n"
                                          "D) [MC_ANSWER4]\n\n"
                                          "Please respond with the letter corresponding to the correct answer choice. "
                                          "Your response should be a single letter and should not include any extra "
                                          "words."
                    },
                "de_from_en": {
                    "gpt-3.5-turbo-0613": "[FLORES_PASSAGE]\n\n"
                                          "[QUESTION]\n\n"
                                          "Option A: [MC_ANSWER1]\n"
                                          "Option B: [MC_ANSWER2]\n"
                                          "Option C: [MC_ANSWER3]\n"
                                          "Option D: [MC_ANSWER4]\n\n"
                                          "Antworten Sie bitte mit \"A\", \"B\", \"C\" oder \"D\", um die richtige "
                                          "Antwort anzugeben. Ihre Antwort sollte nur ein einzelner Buchstabe sein "
                                          "und keine zusätzlichen Wörter enthalten."
                },
                "it_from_en": {
                    "gpt-3.5-turbo-0613": "[FLORES_PASSAGE]\n\n"
                                          "[QUESTION]\n\n"
                                          "Opzione A: [MC_ANSWER1]\n"
                                          "Opzione B: [MC_ANSWER2]\n"
                                          "Opzione C: [MC_ANSWER3]\n"
                                          "Opzione D: [MC_ANSWER4]\n\n"
                                          "Rispondi con \"A\", \"B\", \"C\" o \"D\" per indicare la risposta corretta. "
                                          "La tua risposta deve essere una singola lettera e non deve contenere parole "
                                          "aggiuntive."
                },
                "sv_from_en": {
                    "gpt-3.5-turbo-0613": "[FLORES_PASSAGE]\n\n"
                                          "[QUESTION]\n\n"
                                          "Alternativ A: [MC_ANSWER1]\n"
                                          "Alternativ B: [MC_ANSWER2]\n"
                                          "Alternativ C: [MC_ANSWER3]\n"
                                          "Alternativ D: [MC_ANSWER4]\n\n"
                                          "Vänligen svara med \"A\", \"B\", \"C\" eller \"D\" för att ange det "
                                          "korrekta svaret. Ditt svar ska vara en enda bokstav och får inte innehålla "
                                          "några ytterligare ord."
                },
                "nl_from_en": {
                    "gpt-3.5-turbo-0613": "[FLORES_PASSAGE]\n\n"
                                          "[QUESTION]\n\n"
                                          "Optie A: [MC_ANSWER1]\n"
                                          "Optie B: [MC_ANSWER2]\n"
                                          "Optie C: [MC_ANSWER3]\n"
                                          "Optie D: [MC_ANSWER4]\n\n"
                                          "Antwoord alstublieft met \"A\", \"B\", \"C\" of \"D\" om het juiste "
                                          "antwoord aan te geven. Uw antwoord moet uit één letter bestaan en mag geen "
                                          "extra woorden bevatten.",
                },
            }
        },

        "paws-x": {
            "task_type": "classification",

            "column_names": ("id", "sentence1", "sentence2", "label"),

            "sentence_keys": ("sentence1", "sentence2"),

            "n_labels": 2,

            "multilingual": True,

            "languages": ["de", "en", "es", "fr", "ja", "ko", "zh"],

            "label_to_answer": {
                "en": {0: "no", 1: "yes"},
                "en-paraphrase": {0: "no", 1: "yes"},
                "de_from_en": {0: "nein", 1: "ja"},
                "sv_from_en": {0: "nej", 1: "ja"},
                "it_from_en": {0: "no", 1: "sì"},
                "nl_from_en": {0: "nee", 1: "ja"}
            },

            "answer_to_label": {
                "en": {"no": 0, "yes": 1},
                "en-paraphrase": {"no": 0, "yes": 1},
                "de_from_en": {"nein": 0, "ja": 1},
                "sv_from_en": {"nej": 0, "ja": 1},
                "nl_from_en": {"nee": 0, "ja": 1},
                "it_from_en": {"no": 0, "sì": 1}
            },

            "combine_data": {
                "en": "Sentence 1: \"[SENTENCE1]\"\nSentence 2: \"[SENTENCE2]\"",
                "de": "Satz 1: \"[SENTENCE1]\"\nSatz 2: \"[SENTENCE2]\"",
                "it": "Frase 1: \"[SENTENCE1]\"\nFrase 2: \"[SENTENCE2]\"",
                "nl": "Zin 1: \"[SENTENCE1]\"\nZin 2: \"[SENTENCE2]\"",
                "sv": "Mening 1: \"[SENTENCE1]\"\nMening 2: \"[SENTENCE2]\""
            },

            "instruction": {
                "en": "Do the following two sentences have the same meaning?\n"
                      "Sentence 1: \"[SENTENCE1]\"\n"
                      "Sentence 2: \"[SENTENCE2]\"\n"
                      "Please reply with a single word, either \"yes\" or \"no\".",
                "en-paraphrase": {
                    "gpt-3.5-turbo-0613": "Are the meanings of the following two sentences the same?\n"
                                          "Sentence 1: \"[SENTENCE1]\"\n"
                                          "Sentence 2: \"[SENTENCE2]\"\n"
                                          "Please respond with either \"yes\" or \"no\"."
                },
                "de_from_en": {
                    "gpt-3.5-turbo-0613": "Haben die folgenden beiden Sätze die gleiche Bedeutung?\n"
                                          "Satz 1: \"[SENTENCE1]\"\n"
                                          "Satz 2: \"[SENTENCE2]\"\n"
                                          "Bitte antworten Sie mit einem einzigen Wort, entweder \"ja\" oder \"nein\"."
                },
                "it_from_en": {
                    "gpt-3.5-turbo-0613": "Le seguenti due frasi hanno lo stesso significato?\n"
                                          "Frase 1: \"[SENTENCE1]\"\n"
                                          "Frase 2: \"[SENTENCE2]\"\n"
                                          "Rispondi con una sola parola, \"sì\" o \"no\"."
                },
                "sv_from_en": {
                    "gpt-3.5-turbo-0613": "Har de följande två meningarna samma betydelse?\n"
                                          "Mening 1: \"[SENTENCE1]\"\n"
                                          "Mening 2: \"[SENTENCE2]\"\n"
                                          "Svara med ett enda ord, antingen \"ja\" eller \"nej\"."
                },
                "nl_from_en": {
                    "gpt-3.5-turbo-0613": "Hebben de volgende twee zinnen dezelfde betekenis?\n"
                                          "Zin 1: \"[SENTENCE1]\"\n"
                                          "Zin 2: \"[SENTENCE2]\"\n"
                                          "Antwoord alstublieft met één woord, ofwel \"ja\" ofwel \"nee\"."
                },
            }
        }

    }

}
