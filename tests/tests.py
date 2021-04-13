import sys
sys.path.append("../src")

import pytest
from click.testing import CliRunner
from chat_analyzer import controller


class Tests:
    def test_percentage_all(self):
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


    def test_percentage_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chat.txt', '-p', '-u', 'A'])
        expected_res = '''Total Count: 39939

Message Count: 6872
Percentage: 17.206239515260773
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_conv_starters_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chat.txt', '-cS'])
        expected_res = '''The user C started consversation 255 time(s)
The user E started consversation 159 time(s)
The user A started consversation 302 time(s)
The user D started consversation 283 time(s)
The user B started consversation 187 time(s)
The user F started consversation 89 time(s)
The user G started consversation 4 time(s)
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_conv_starters_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chat.txt', '-cS', '-u', 'A'])
        expected_res = '''The user A started consversation 302 time(s)
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_activity_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chat.txt', '-a'])
        expected_res = '''The user A mostly stays active around 15 Hours
The user B mostly stays active around 15 Hours
The user C mostly stays active around 15 Hours
The user D mostly stays active around 15 Hours
The user E mostly stays active around 15 Hours
The user F mostly stays active around 14 Hours
The user G mostly stays active around 18 Hours
The user H mostly stays active around 21 Hours
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_activity_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chat.txt', '-a', '-u', 'A'])
        expected_res = '''The user A mostly stays active around 15 Hours
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_interaction_curve_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chat.txt', '-iC'])
        expected_res = '''The interactions in this chat have increased!
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_interaction_curve_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chat.txt', '-iC', '-u', 'A'])
        expected_res = '''Your interactions in this chat have increased!
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]
