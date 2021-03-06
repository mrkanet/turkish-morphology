# coding=utf-8
# Copyright 2019 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for src.analyzer.morphotactics.reader."""

import collections
import os

from src.analyzer.morphotactics import reader

from absl.testing import absltest
from absl.testing import parameterized

_TESTDATA_DIR = "src/analyzer/morphotactics/testdata"


def _read_file(path):
  with open(path, "r") as f:
    read = f.read()
  return read


class ReadRuleDefinitionsTest(parameterized.TestCase):

  def test_success(self):
    path = os.path.join(_TESTDATA_DIR, "morphotactics_valid_rules_1.txt")
    actual = reader.read_rule_definitions(path)
    expected = collections.OrderedDict((
        (7, ["JJ", "STATE-2", "<eps>", "<ePs>"]),
        (8, ["IN", "STATE-3", "<EpS>", "<eps>"]),
        (12, ["DERIVED-STATE-2", "STATE-2", "<eps>", "<EPS>"]),
        (18, ["state-3", "STATE-9", "<EPS>", "<eps>"]),
        (21, ["STATE-5", "StAtE-7", "+DA[Case=Loc]", "+DA"]),
        (22, ["STATE-6", "STATE-8", "+HmHz[Possessive=P1pl]", "+HmHz"]),
        (25, ["StAtE-8", "state-10", "1[CD]", "1*ir*"]),
        (31,
         ["STATE-9", "DERIVED-STATE-1", ")([JJ]-cHk[Derivation=Dim]", "+cHk"]),
        (35, ["STATE-11", "ACCEPT", ")+[Proper=True]", "<eps>"]),
    ))
    self.assertDictEqual(expected, actual)

  @parameterized.named_parameters([
      {
          "testcase_name": "InvalidPath",
          "path": os.path.join(_TESTDATA_DIR, "invalid_path.tsv"),
          "error": IOError,
      },
      {
          "testcase_name": "EmptyPath",
          "path": "",
          "error": IOError,
      },
  ])
  def test_raises_exception(self, path, error):
    with self.assertRaises(error):
      reader.read_rule_definitions(path)


if __name__ == "__main__":
  absltest.main()
