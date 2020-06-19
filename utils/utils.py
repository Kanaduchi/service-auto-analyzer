"""
* Copyright 2019 EPAM Systems
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
"""

import re
import string
import nltk
import logging
from dateutil.parser import parse
import urllib
from urllib.parse import urlparse
import warnings

logger = logging.getLogger("analyzerApp.utils")
file_extensions = ["java", "php", "cpp", "cs", "c", "h", "js", "swift", "rb", "py", "scala"]
stopwords = set(nltk.corpus.stopwords.words("english"))


def ignore_warnings(method):
    """Decorator for ignoring warnings"""
    def _inner(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = method(*args, **kwargs)
        return result
    return _inner


def sanitize_text(text):
    """Sanitize text by deleting all numbers"""
    return re.sub(r"\d+", "", text)


def calculate_line_number(text):
    """Calculate line numbers in the text"""
    return len([line for line in text.split("\n") if line.strip() != ""])


def first_lines(log_str, n_lines):
    """Take n first lines"""
    return "\n".join((log_str.split("\n")[:n_lines])) if n_lines >= 0 else log_str


def build_url(main_url, url_params):
    """Build url by concating url and url_params"""
    return main_url + "/" + "/".join(url_params)


def delete_empty_lines(log):
    """Delete empty lines"""
    return "\n".join([line for line in log.split("\n") if line.strip() != ""])


def reverse_log(log):
    """Concatenates lines in reverse order"""
    return "\n".join(log.split("\n")[::-1])


def split_words(text, min_word_length=0, only_unique=True, split_urls=True):
    all_unique_words = set()
    all_words = []
    translate_map = {}
    for punct in string.punctuation + "<>{}[];=()'\"":
        if punct != "." and (split_urls or punct not in ["/", "\\"]):
            translate_map[punct] = " "
    text = text.translate(text.maketrans(translate_map)).strip().strip(".")
    for word_part in text.split():
        word_part = word_part.strip().strip(".").lower()
        for w in word_part.split():
            if w != "" and len(w) >= min_word_length:
                if w in stopwords:
                    continue
                if not only_unique or w not in all_unique_words:
                    all_unique_words.add(w)
                    all_words.append(w)
    return all_words


def transform_string_feature_range_into_list(text):
    """Converts features from string to list of ids"""
    values = []
    for part in text.split(","):
        if part.strip() == "":
            continue
        if "-" in part:
            start, end = part.split("-")[:2]
            values.extend(list(range(int(start), int(end) + 1)))
        else:
            values.append(int(part))
    return values


def remove_starting_datetime(text, remove_first_digits=False):
    """Removes datetime at the beginning of the text"""
    log_date = ""
    idx_text_start = 0
    for idx, str_part in enumerate(text.split(" ")):
        try:
            parse(log_date + " " + str_part)
            log_date = log_date + " " + str_part
            log_date = log_date.strip()
        except Exception as e: # noqa
            idx_text_start = idx
            break
    log_date = log_date.replace("'", "").replace("\"", "")
    if re.search(r"\d{1,7}", log_date) and re.search(r"\d{1,7}", log_date).group(0) == log_date:
        idx_text_start = 0

    text_split = text.split(" ")
    if remove_first_digits:
        if idx_text_start == 0:
            for idx in range(len(text_split)):
                rs = text_split[idx].translate(text_split[idx].maketrans("", "", string.punctuation))
                if not re.search(r"\d+", rs.strip()):
                    idx_text_start = idx
                    break

    return " ".join(text_split[idx_text_start:])


def delete_line_numbers(text):
    """Deletes line numbers in the stacktrace"""
    text = re.sub(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)", r"\g<1>#\g<2>", text)

    res = re.sub(r"(?<=:)\d+(?=\)?\]?(\n|\r\n|$))", " ", text)
    res = re.sub(r"((?<=line )|(?<=line))\s*\d+\s*((?=, in)|(?=,in)|(?=\n)|(?=\r\n)|(?=$))",
                 " ", res, flags=re.I)
    res = re.sub("|".join([r"\.%s(?!\.)\b" % ext for ext in file_extensions]), " ", res, flags=re.I)
    res = re.sub(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})#(\d+)", r"\g<1>:\g<2>", res)
    result = re.search(r"^\s*at\s+.*\(.*?\)[\s]*$", res)
    if result and result.group(0) == res:
        res = re.sub(r"\d", "", res)
        res = "# " + res
    else:
        result = re.search(r"^\s*\w+([\.\/]\s*\w+)+\s*\(.*?\)[\s]*$", res)
        if result and result.group(0) == res:
            res = "# " + res
    return res


def find_only_numbers(detected_message_with_numbers):
    """Removes all non digit symbols and concatenates unique numbers"""
    detected_message_only_numbers = re.sub(r"[^\d \._]", "", detected_message_with_numbers)
    return " ".join(split_words(detected_message_only_numbers, only_unique=True))


def is_python_log(log):
    """Tries to find whether a log was for the python language"""
    found_file_extensions = []
    for file_extension in file_extensions:
        if re.search(r"\.%s(?!\.)\b" % file_extension, log):
            found_file_extensions.append(file_extension)
    if len(found_file_extensions) == 1 and found_file_extensions[0] == "py":
        return True
    return False


def reverse_log_if_needed(message):
    if is_python_log(message):
        return reverse_log(message)
    return message


def has_stacktrace_keywords(line):
    normalized_line = line.lower()
    for key_word in ["stacktrace", "stack trace", "stack-trace", "traceback"]:
        if re.search(r"\s*%s\s*:\s*$" % key_word, normalized_line):
            return True
        if "end of " in normalized_line and key_word in normalized_line:
            return True
    return False


def has_more_lines_pattern(line):
    normalized_line = line.lower().strip()
    result = re.search(r"^\s*\.+\s*\d+\s+more\s*$", normalized_line)
    if result and result.group(0) == normalized_line:
        return True
    return False


def detect_log_description_and_stacktrace(message, default_log_number=1, max_log_lines=5):
    """Split a log into a log message and stacktrace"""
    message = delete_empty_lines(message)
    if default_log_number == -1:
        return message, ""
    if calculate_line_number(message) > 2:
        split_lines = message.split("\n")
        detected_message_lines = []
        stacktrace_lines = []
        for idx, line in enumerate(split_lines):
            modified_line = delete_line_numbers(line)
            if has_stacktrace_keywords(line) or has_more_lines_pattern(line):
                continue
            if modified_line != line:
                stacktrace_lines.append(line)
            else:
                detected_message_lines.append(line)

        if len(detected_message_lines) == len(split_lines):
            stacktrace_lines = detected_message_lines[max_log_lines:]
            detected_message_lines = detected_message_lines[:max_log_lines]

        if len(detected_message_lines) < default_log_number:
            all_message = detected_message_lines + stacktrace_lines
            detected_message_lines = all_message[:default_log_number]
            stacktrace_lines = all_message[default_log_number:]

        return "\n".join(detected_message_lines), "\n".join(stacktrace_lines)
    return message, ""


def fix_big_encoded_urls(message):
    """Decodes urls encoded with %12 and etc. and removes brackets to separate url"""
    try:
        new_message = urllib.parse.unquote(message)
    except: # noqa
        pass
    if new_message != message:
        return re.sub(r"[\(\)\{\}#%]", " ", new_message)
    return message


def choose_fields_to_filter(filter_min_should_match, log_lines):
    if filter_min_should_match:
        return ["detected_message", "message"] if log_lines == -1 else ["message"]
    return []


def leave_only_unique_lines(message):
    all_unique = set()
    all_lines = []
    for idx, line in enumerate(message.split("\n")):
        # To remove lines with 'For documentation on this error please visit ...url'
        if "documentation" in line.lower() and "error" in line.lower() and "visit" in line.lower():
            continue
        if line.strip() not in all_unique:
            all_unique.add(line.strip())
            all_lines.append(line)
    return "\n".join(all_lines)


def remove_generated_parts(message):
    """Removes lines with '<generated>' keyword and removes parts, like $ab24b, @c321e from words"""
    all_lines = []
    for line in message.split("\n"):
        if "<generated>" in line.lower():
            continue
        if has_stacktrace_keywords(line) or has_more_lines_pattern(line):
            continue
        for symbol in [r"\$", "@"]:
            all_found_parts = set()
            for m in re.finditer(r"%s+(.+?)\b" % symbol, line):
                found_part = m.group(1).strip().strip(symbol).strip()
                if found_part != "":
                    all_found_parts.add((found_part, m.group(0).strip()))
            sorted_parts = sorted(list(all_found_parts), key=lambda x: len(x[1]), reverse=True)
            for found_part in sorted_parts:
                whole_found_part = found_part[1].replace("$", r"\$")
                found_part = found_part[0]
                part_to_replace = ""
                if re.search(r"\d", found_part):
                    part_with_numbers_in_the_end = re.search(r"[a-zA-z]{5,}\d+", found_part)
                    if part_with_numbers_in_the_end and part_with_numbers_in_the_end.group(0) == found_part:
                        part_to_replace = " %s" % found_part
                    else:
                        part_to_replace = ""
                else:
                    part_to_replace = ".%s" % found_part
                try:
                    line = re.sub(whole_found_part, part_to_replace, line)
                except: # noqa
                    pass

        line = re.sub(r"\.+", ".", line)
        all_lines.append(line)
    return "\n".join(all_lines)


def clean_text_from_html_tags(message):
    """Removes style and script tags together with inner text and removes html tags"""
    regex_style_tag = re.compile('<style.*?>[\\s\\S]*?</style>')
    message = re.sub(regex_style_tag, " ", message)
    regex_script_tag = re.compile('<script.*?>[\\s\\S]*?</script>')
    message = re.sub(regex_script_tag, " ", message)
    regex_html_tags = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    message = re.sub(regex_html_tags, " ", message)
    return message


def clean_html(message):
    """Removes html tags inside the parts with <.*?html.*?>...</html>"""
    all_lines = []
    started_html = False
    finished_with_html_tag = False
    html_part = []
    for idx, line in enumerate(message.split("\n")):
        if re.search(r"<.*?html.*?>", line):
            started_html = True
            html_part.append(line)
        else:
            if started_html:
                html_part.append(line)
            else:
                all_lines.append(line)
        if "</html>" in line:
            finished_with_html_tag = True
        if finished_with_html_tag:
            all_lines.append(clean_text_from_html_tags("\n".join(html_part)))
            html_part = []
            finished_with_html_tag = False
            started_html = False
    if len(html_part) > 0:
        all_lines.extend(html_part)
    return delete_empty_lines("\n".join(all_lines))


def replace_tabs_for_newlines(message):
    return message.replace("\t", "\n")


def remove_credentials_from_url(url):
    parsed_url = urlparse(url)
    new_netloc = re.sub("^.+?:.+?@", "", parsed_url.netloc)
    return url.replace(parsed_url.netloc, new_netloc)
