#   Copyright 2023 EPAM Systems
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   https://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
from typing import List

from app.utils.utils import read_json_file


def get_fixture(fixture_name, to_json=False):
    return read_json_file("test_res/fixtures", fixture_name, to_json)


def read_file_lines(folder: str, filename: str) -> List[str]:
    with open(os.path.join(folder, filename), "r") as file:
        return file.readlines()
