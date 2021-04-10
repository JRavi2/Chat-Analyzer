import sys
sys.path.append("../src")

import pytest
from click.testing import CliRunner
from chat_analyzer import controller


def test_percentage():
    runner = CliRunner()
    res = runner.invoke(controller, ['test_chat.txt', '-p'])
    expected_res = '''Total Count: 39939

For the user A
Message Count: 6872
Percentage: 17.206239515260773

For the user B
Message Count: 7012
Percentage: 17.55677408047272

For the user C
Message Count: 9260
Percentage: 23.18535767044743

For the user D
Message Count: 8518
Percentage: 21.327524474824106

For the user E
Message Count: 6456
Percentage: 16.1646510929167

For the user F
Message Count: 1776
Percentage: 4.446781341545857

For the user G
Message Count: 44
Percentage: 0.11016800620946944

For the user H
Message Count: 1
Percentage: 0.0025038183229424875

Program Finished'''
    assert expected_res == res.output[:res.output[:-1].rfind('\n')]

