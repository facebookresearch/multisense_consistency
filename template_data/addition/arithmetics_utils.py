"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""

numbers_sv = {
    "0": "noll", "1": "ett", "2": "två", "3": "tre", "4": "fyra", "5": "fem", "6": "sex", "7": "sju", "8": "åtta",
    "9": "nio", "10": "tio", "11": "elva", "12": "tolv", "13": "tretton", "14": "fjorton", "15": "femton",
    "16": "sexton", "17": "sjutton", "18": "arton", "19": "nitton", "20": "tjugo", "30": "trettio", "40":
    "fyrtio", "50": "femtio", "60": "sextio", "70": "sjuttio", "80": "åttio", "90": "nittio", "100": "hundra"
}

numbers_de = {
    "0": "null", "1": "ein", "2": "zwei", "3": "drei", "4": "vier", "5": "fünf", "6": "sechs", "7": "sieben",
    "8": "acht", "9": "neun", "10": "zehn", "11": "elf", "12": "zwölf", "13": "dreizehn", "14": "vierzehn",
    "15": "fünfzehn", "16": "sechzehn", "17": "siebzehn", "18": "achtzehn", "19": "neunzehn", "20": "zwanzig",
    "30": "dreißig", "40": "vierzig", "50": "fünfzig", "60": "sechzig", "70": "siebzig", "80": "achtzig",
    "90": "neunzig", "100": "hundert"
}

numbers_en = {
    "0": "zero", "1": "one", "2": "two",  "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8":
    "eight", "9": "nine", "10": "ten", "11": "eleven", "12": "twelve", "13": "thirteen", "14": "fourteen",
    "15": "fifteen", "16": "sixteen", "17": "seventeen", "18": "eighteen", "19": "nineteen", "20": "twenty",
    "30": "thirty", "40": "forty", "50": "fifty", "60": "sixty", "70": "seventy", "80": "eighty",
    "90": "ninety", "100": "hundred", "1000": "thousand"
}

numbers_nl = {
    "0": "nul", "1": "één", "2": "twee", "3": "drie", "4": "vier", "5": "vijf", "6": "zes", "7": "zeven",
    "8": "acht", "9": "negen", "10": "tien", "11": "elf", "12": "twaalf", "13": "dertien", "14": "veertien",
    "15": "vijftien", "16": "zestien", "17": "zeventien", "18": "achttien", "19": "negentien", "20": "twintig",
    "30": "dertig", "40": "veertig", "50": "vijftig", "60": "zestig", "70": "zeventig", "80": "tachtig",
    "90": "negentig", "100": "honderd"
}

numbers_it = {
    "0": "zero", "1": "uno", "2": "due", "3": "tre", "4": "quattro", "5": "cinque", "6": "sei", "7": "sette",
    "8": "otto", "9": "nove", "10": "dieci", "11": "undici", "12": "dodici", "13": "tredici", "14": "quattordici",
    "15": "quindici", "16": "sedici", "17": "diciassette", "18": "diciotto", "19": "diciannove", "20": "venti",
    "23": "ventitré", "30": "trenta", "33": "trentatré", "40": "quaranta", "43": "quarantatré", "50": "cinquanta",
    "53": "cinquantatré", "60": "sessanta", "63": "sessantatré", "70": "settanta", "73": "settantatré", "80": "ottanta",
    "83": "ottantatré", "90": "novanta", "93": "novantatré", "100": "cento"
}


def number_to_words(language, input_number): 
    
    number_string = str(input_number)
    
    if language == "en":      
        return english_number_generator(number_string)
    elif language == "de":
        return german_number_generator(number_string)
    elif language == "sv":
        return swedish_number_generator(number_string)
    elif language == "it":
        return italian_number_generator(number_string)
    elif language == "nl":
        return dutch_number_generator(number_string)
    else:
        print("invalid language")


def dutch_number_generator(input_number):
    def from_three_digits(input_number, actual_length):

        output_number = ""

        if len(input_number) == 3:
            if sum([int(i) for i in input_number]) != 0:
                if input_number[0] != "0":
                    if input_number[0] == "1":
                        output_number += "honderd"
                    else:
                        output_number += numbers_nl[input_number[0]] + "honderd"
                input_number = input_number[1:]
            else:
                input_number = ""

        if len(input_number) == 2:
            if input_number in numbers_nl.keys():
                output_number += numbers_nl[input_number]
                input_number = ""
            elif input_number == "00":
                input_number = ""
            elif input_number[0] == "0":
                input_number = input_number[1:]
            else:
                output_number += numbers_nl[input_number[1]]
                if output_number[-1] == "e":
                    output_number += "ën" + numbers_nl[input_number[0] + "0"]
                else:
                    output_number += "en" + numbers_nl[input_number[0] + "0"]

        if len(input_number) == 1:
            if actual_length < 4 and input_number == "1":
                output_number += "één"
            else:
                output_number += numbers_nl[input_number]
        if "één" in output_number and len(output_number) > 3:
            output_number = output_number.replace("één", "een")

        return output_number

    output_number = ""
    n_digits = len(input_number)
    if len(input_number) > 3:
        if input_number[0:-3] == "1":
            output_number += "duizend"
        else:
            output_number += from_three_digits(input_number[0:-3], n_digits) + "duizend"
    if sum([int(i) for i in input_number[-3:]]) > 0:
        if len(input_number) > 3:
            output_number += " "
        output_number += from_three_digits(input_number[-3:], len(input_number[-3:]))
    if input_number == "0":
        output_number = "nul"

    return output_number
        

def alternative_formulation(language, number_in_words):
    
    alternatives = []
    
    if language == "de":
        if "eintausend" in number_in_words:
            replace_thousand = number_in_words.replace("eintausend", "tausend")
            alternatives.append(replace_thousand)
        collection = [number_in_words] + alternatives
        for elem in collection:
            if "tausend" in elem and not elem[-7:] == "tausend":
                alternatives.append(elem.replace("tausend", "tausendund"))
        if "einhundert" in number_in_words:
            replace_hundred = number_in_words.replace("einhundert", "hundert")
            alternatives.append(replace_hundred)
        collection = [number_in_words] + alternatives
        for elem in collection:
            if "hundert" in elem and not elem[-7:] == "hundert":
                alternatives.append(elem.replace("hundert", "hundertund"))
        if "eintausend" in number_in_words and "einhundert" in number_in_words:
            replace_both = replace_thousand.replace("einhundert", "hundert")
            alternatives.append(replace_both)
    if language == "nl":
        if "honderd" in number_in_words and not number_in_words[-7:] == "honderd":
            alternatives.append(number_in_words.replace("honderd", "honderden"))
            alternatives.append(number_in_words.replace("honderd", "honderd "))
        collection = [number_in_words] + alternatives
        for elem in collection:
            if "één" in elem:
                alternatives.append(elem.replace("één", "een"))
            if "een" in elem:
                alternatives.append(elem.replace("een", "één"))
    if language == "it":
        if "tré" == number_in_words[-3:]:
            alternatives.append(number_in_words[:-3] + "tre")
        if "tre" == number_in_words[-3:]:
            alternatives.append(number_in_words[-3] + "tré")
        if "centouno" in number_in_words:
            alternatives.append(number_in_words.replace("centouno", "centuno"))
        if "centootto" in number_in_words:
            alternatives.append(number_in_words.replace("centootto", "centotto"))
    if language == "en":
        if "one thousand" in number_in_words:
            replace_thousand = number_in_words.replace("one thousand", "thousand")
            alternatives.append(replace_thousand)
        if "one hundred" in number_in_words:
            replace_hundred = number_in_words.replace("one hundred", "hundred")
            alternatives.append(replace_hundred)
        if "one_thousand" in number_in_words and "one hundred" in number_in_words:
            replace_both = replace_thousand.replace("one hundred", "hundred")
            alternatives.append(replace_both)
    if language == "sv":
        if "ettusen" in number_in_words:
            replace_thousand = number_in_words.replace("ettusen", "tusen")
            alternatives.append(replace_thousand)
            wrong_spelling = number_in_words.replace("ettusen", "etttusen")
            alternatives.append(wrong_spelling)
        if "etthundra" in number_in_words:
            replace_hundred = number_in_words.replace("etthundra", "hundra")
            alternatives.append(replace_hundred)
        if "ettusen" in number_in_words and "etthundra" in number_in_words:
            replace_both = replace_thousand.replace("etthundra", "hundra")
            alternatives.append(replace_both)
        if "tusen" in number_in_words:
            collection = [number_in_words] + alternatives
            for elem in collection:
                alternatives.append(elem.replace(" ", ""))

    return alternatives


def italian_number_generator(input_number):
    def from_three_digits(input_number):

        output_number = ""

        if len(input_number) == 3:
            if sum([int(i) for i in input_number]) != 0:
                if input_number[0] != "0":
                    if input_number[0] == "1":
                        output_number += "cento"
                    else:
                        output_number += numbers_it[input_number[0]] + "cento"
                input_number = input_number[1:]
            else:
                input_number = ""

        if len(input_number) == 2:
            if input_number in numbers_it.keys():
                output_number += numbers_it[input_number]
                input_number = ""
            elif input_number == "00":
                input_number = ""
            elif input_number[0] == "0":
                input_number = input_number[1:]
            else:
                output_number += numbers_it[input_number[0] + "0"]
                input_number = input_number[1:]
                if input_number == "1" or input_number == "8":
                    output_number = output_number[:-1]

        if len(input_number) == 1:
            output_number += numbers_it[input_number]

        return output_number

    output_number = ""
    if len(input_number) > 3:
        if input_number[0:-3] == "1":
            output_number += "mille"
        else:
            output_number += from_three_digits(input_number[0:-3]) + "mila"
    if sum([int(i) for i in input_number[-3:]]) > 0:
        output_number += from_three_digits(input_number[-3:])
    if input_number == "0":
        output_number = "zero"

    return output_number


def swedish_number_generator(input_number):

    def from_three_digits(input_number):
        output_number = ""
        if len(input_number) == 3:
            if sum([int(i) for i in input_number]) != 0:
                if input_number[0] != "0":
                    output_number += numbers_sv[input_number[0]] + "hundra"
                input_number = input_number[1:]
            else:
                input_number = ""
        if len(input_number) == 2:
            if not sum([int(i) for i in input_number]) == 0:
                if input_number in numbers_sv.keys():
                    output_number += numbers_sv[input_number]
                    input_number = ""
                elif input_number[0] != "0":
                    output_number += numbers_sv[input_number[0] + "0"]
                    input_number = input_number[1:]
                else:
                    input_number = input_number[1:]
            else:
                input_number = ""
        if len(input_number) == 1:
            output_number += numbers_sv[input_number]
        return output_number

    output_number = ""
    n_digits = len(input_number)
    if n_digits > 3:
        if from_three_digits(input_number[0:-3]) != "ett":
            output_number += from_three_digits(input_number[0:-3]) + "tusen"
        else:
            output_number += "ettusen"

    if sum([int(i) for i in input_number[-3:]]) > 0:
        if n_digits > 3:
            output_number += " "
        output_number += from_three_digits(input_number[-3:])

    return output_number


def german_number_generator(input_number):

    def from_three_digits(input_number, actual_length):
        output_number = ""
        if len(input_number) == 3:
            if sum([int(i) for i in input_number]) != 0:
                if input_number[0] != "0":
                    output_number += numbers_de[input_number[0]] + "hundert"
                input_number = input_number[1:]
            else:
                input_number = ""
        if len(input_number) == 2:
            if input_number in numbers_de.keys():
                output_number += numbers_de[input_number]
                input_number = ""
            elif input_number == "00":
                input_number = ""
            elif input_number[0] == "0":
                input_number = input_number[1:]
            else:
                output_number += numbers_de[input_number[1]]
                if input_number[0] != "0":
                    output_number += "und" + numbers_de[input_number[0] + "0"]
                else:
                    output_number += numbers_de[input_number[1]]
                    input_number = ""
        if len(input_number) == 1:
            if actual_length < 4 and input_number == "1":
                output_number += "eins"
            else:
                output_number += numbers_de[input_number]
        return output_number

    output_number = ""
    n_digits = len(input_number)
    if len(input_number) > 3:
        output_number += from_three_digits(input_number[0:-3], n_digits) + "tausend"
    if sum([int(i) for i in input_number[-3:]]) > 0:
        output_number += from_three_digits(input_number[-3:], len(input_number[-3:]))

    return output_number


def english_number_generator(input_number):

    def from_three_digits(input_number, actual_length):
        output_number = ""
        second_to_last_zero = False
        if len(input_number) == 3:
            if sum([int(i) for i in input_number]) != 0:
                if input_number[0] != "0":
                    if len(output_number) > 1:
                        output_number += " "
                    output_number += numbers_en[input_number[0]] + " hundred"
                input_number = input_number[1:]
            else:
                input_number = ""
        if len(input_number) == 2:
            if len(output_number) > 1 and sum([int(i) for i in input_number]) != 0:
                output_number += " "
            if input_number in numbers_en.keys():
                output_number += numbers_en[input_number]
                input_number = ""
            elif input_number[0] != "0":
                output_number += numbers_en[input_number[0] + "0"] + "-"
                input_number = input_number[1:]
            elif input_number == "00":
                input_number = ""
            elif input_number[0] == "0":
                input_number = input_number[1:]
                second_to_last_zero = True
        if len(input_number) == 1:
            if second_to_last_zero and actual_length < 4:
                output_number += "and " 
            output_number += numbers_en[input_number]
        return output_number

    output_number = ""
    n_digits = len(input_number)
    if len(input_number) > 3:
        output_number += from_three_digits(input_number[0:-3], n_digits) + " thousand"
    if sum([int(i) for i in input_number[-3:]]) != 0:
        if n_digits > 3:
            output_number += " "
        output_number += from_three_digits(input_number[-3:], len(input_number[-3:]))

    return output_number
