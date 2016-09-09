import sublime
import sublime_plugin
import re
import os
import random
from operator import itemgetter
from .edit import *

random.seed(1)

obj = {'levelStack': [0], 'valueStack': [''], 'delimiter': '.'}
autoDetectIndentPattern = False


class ConvertCaseCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        next_case = ""
        for region in self.view.sel():
            if not region.empty():
                word = self.view.substr(region)
                if next_case == "":
                    print("")
                    print("Word taken as sample: " + word)
                    next_case = get_next_case(word)
                    print(next_case)
                text = convert_to_next_case(word, next_case)
                self.view.replace(edit, region, text)


class FlattenYamlCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        entire_text_region = sublime.Region(0, self.view.size())
        text = flatten_yaml_text(self.view.substr(entire_text_region))
        self.view.replace(edit, entire_text_region, text)


class PadRightCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        selections = []   # (text, region, start_col, end_col)

        for region in self.view.sel():
            selections.append((self.view.substr(region),
                               region,
                               self.view.rowcol(region.a)[1],
                               self.view.rowcol(region.b)[1]))
        max_end_col = max([end_col for (_, _, _, end_col) in selections])
        padding = [' ' * (max_end_col - end_col)
                   for (text, region, _, end_col) in selections]
        padding.reverse()
        for region in self.view.sel():
            p = padding.pop()
            self.view.replace(edit, region, self.view.substr(region) + p)


class IntersectSelectionCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        index = -1
        for region in self.view.sel():
            index = index + 1
            if region.empty():
                self.view.replace(edit, self.view.sel()[0], "")
            text = self.view.substr(region)
            cur_lines = text.split('\n')
            if index == 0:
                intersected_lines = cur_lines
                continue
            lines = intersected_lines
            for line in intersected_lines:
                if line not in cur_lines:
                    lines.remove(line)
            intersected_lines = lines
        index = -1
        for region in self.view.sel():
            index = index + 1
            if index == 0:
                self.view.replace(edit, region, '\n'.join(lines))
            else:
                self.view.replace(edit, region, '')


# sort and then run this command
# runs on entire file
class GroupByAndCountCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        entire_text_region = sublime.Region(0, self.view.size())
        text = group_by_count_text(self.view.substr(entire_text_region))
        self.view.replace(edit, entire_text_region, text)


def group_by_count_text(text):
    d = {}
    lines = text.split(os.linesep)
    for line in lines:
        d[line] = (d.get(line) or 0) + 1
    return os.linesep.join(
        '%s %s' % (v, k) for (k, v) in
        sorted(d.items(), key=itemgetter(1), reverse=True))


def indentLevel(text):
    if (obj.get('indent') is None):
        m = re.match("^[ \t]+", text)
        if (m):
            obj['indent'] = text[m.start():m.end()]
            return 1
        else:
            return 0
    level = 0
    if autoDetectIndentPattern:
        p = obj['indent']
    else:
        p = ' '
    m = re.match(p, text)
    while(m):
        text = text[m.end():]
        level = level + 1
        m = re.match(p, text)
    return level


def getLevel():
    return obj['levelStack'][-1]


def flatten_yaml_text(text):
    lines = text.split('\n')
    flattened = []
    for line in lines:
        value = line.strip()
        if(value == ""):
            flattened.append('\n')
            continue
        if(value[0] == "#"):
            flattened.append('\n')
            continue
        level = indentLevel(line)
        while(getLevel() > level):
            obj['levelStack'].pop()
            obj['valueStack'].pop()
        if(level > getLevel()):
            obj['levelStack'].append(level)
        else:
            obj['valueStack'].pop()
        value = re.sub(':[ ]*$', '', value)
        obj['valueStack'].append(value.strip())

        flattened.append(obj.get('delimiter').join(obj['valueStack']) + "\n")
    return ''.join(flattened)[0:-1]


# def isCharacter(c):
#     return c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z'


# def isNumeric(c):
#     return c >= '0' and c <= '9'


# def isUpper(c):
#     return c >= 'A' and c <= 'Z'


# def isLower(c):
#     return c >= 'a' and c <= 'z'


# def isPunctuation(c):
#     return not (isNumeric(c) or isCharacter(c))


# def isUnderscore(c):
#     return c == '_'


# def get_components1(word):
#     methods = [isCharacter, isUpper, isNumeric, isUnderscore, isPunctuation]
#     data = map(lambda x: map(lambda y: y(x), methods), word)

#     startPoints1 = [i for previous, last, dataEntry, i, ch in zip([[], []] + data, [[]] + data, data, range(0, len(word)), word)
#                     if not last == dataEntry and not previous == dataEntry and not isPunctuation(ch)]

#     [zip(startPoints1,startPoints1+[])]

#     previous = []
#     last = []
#     startPoints2 = []
#     for i, dataEntry in enumerate(data):
#         print(previous, last, dataEntry, i)
#         if not last == dataEntry and not previous == dataEntry:
#             if not isPunctuation(word[i]):
#                 startPoints2.append(i)
#         previous = last
#         last = dataEntry

#     return (startPoints1 == startPoints2, startPoints1, startPoints2)


# def get_case_index(word):
#     for ch in word:
#         if()


def get_components(word):
    retain_beginning_underscores = True
    if retain_beginning_underscores:
        regex = "([a-z]+|[A-Z][a-z]+|[a-zA-Z]+|[A-Z]+|[0-9]+|^[^a-zA-Z]+)"
    else:
        regex = "([a-z]+|[A-Z][a-z]+|[a-zA-Z]+|[A-Z]+|[0-9]+)"
    # return [(m.group(0), m.start(), m.end()) for m in re.finditer(regex, word)]
    return [m.group(0) for m in re.finditer(regex, word)]


def join_with_underscore(components):
    components=list(components)
    if not components[0][0].isalnum():
        return components[0] + '_'.join(components[1:])
    return '_'.join(components)


def to_camel_case(word):
    components = get_components(word)
    if not components[0][0].isalpha():
        return components[0] + ''.join(c.lower() if i == 0 else c.title() for i, c in enumerate(components[1:]))
    return ''.join(c.lower() if i == 0 else c.title() for i, c in enumerate(components))


def to_snake_case(word):
    return join_with_underscore(c.lower() for i,c in enumerate(get_components(word)))


def to_cs_case(word):
    return ''.join(c.title() for i,c in enumerate(get_components(word)))


def to_all_caps(word):
    return join_with_underscore(c.upper() for i,c in enumerate(get_components(word)))


# [
# "helloWorld", # camel case
# "hello_world", # snake case 
# "HelloWorld", # cs case 
# "HELLO_WORLD", # const case / all caps
# ]

def first_letter_small(word):
    # check the case of first alphabetic character not simply the first character
    r = next(c for c in word if c.isalpha()).islower()
    if r:
        print("first letter is small")
    else:
        print("first letter is caps")
    return r


def contains_underscore(word):
    # TODO: need to ignore the initial underscores(or any symbols) if any while checking
    r = '_' in re.sub("^[^a-zA-Z]*", "", word)
    if r:
        print("contains underscore")
    else:
        print("does not contain underscore")
    return r


def contains_small_characters(word):
    r = any(filter(str.islower, word))
    if r:
        print("contains small chars")
    else:
        print("does not contain small chars")
    return r


def contains_capital_characters(word):
    r = any(filter(str.isupper, word))
    if r:
        print("contains capital chars")
    else:
        print("does not contain capital chars")
    return r


def transform_to_tokens(word):
    fns = [first_letter_small, contains_underscore, contains_small_characters, contains_capital_characters]
    return tuple(fn(word) for fn in fns)


# 0 camel case
# 1 snake case
# 2 cs case
# 3 all caps
# 4 close to snake case

actions_map = {
    (True,True,True,True):{"current_case":4, "case_name": "close to snake case", "next_case":1},
    (True,True,True,False):{"current_case":1, "case_name": "snake case", "next_case":2},
    (True,False,True,True):{"current_case":0, "case_name": "camel case", "next_case":1},
    (True,False,True,False):{"current_case":0, "case_name": "camel case", "next_case":1},
    (False,True,True,True):{"current_case":4, "case_name": "close to snake case", "next_case":1},
    (False,True,False,True):{"current_case":3, "case_name": "all caps case", "next_case":0},
    (False,False,True,True):{"current_case":2, "case_name": "cs case", "next_case":3},
    (False,False,False,True):{"current_case":3, "case_name": "all caps case", "next_case":0},
}

convert_case_actions = [
    to_camel_case,
    to_snake_case,
    to_cs_case,
    to_all_caps,
]


def get_next_case(word):
    case_details = actions_map[transform_to_tokens(word)]
    print("   Detected as " + case_details["case_name"])
    print("   will be converted using " + str(convert_case_actions[case_details["next_case"]]))
    return case_details["next_case"]

def convert_to_next_case(word, next_case):
    return convert_case_actions[next_case](word)
