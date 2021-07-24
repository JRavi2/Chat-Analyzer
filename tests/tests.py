import sys

from click.testing import CliRunner

from chat_analyzer import controller

sys.path.append("../src")


class Test_WA:
    """The main test class for Whatsapp chat exports"""

    def test_percentage_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-p'])
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
        res = runner.invoke(controller, ['test_chats/wa.txt', '-p', '-u', 'A'])
        expected_res = '''Total Count: 39939

Message Count: 6872
Percentage: 17.206239515260773
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_conv_starters_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-cS'])
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
        res = runner.invoke(controller, ['test_chats/wa.txt', '-cS', '-u', 'A'])
        expected_res = '''The user A started consversation 302 time(s)
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_activity_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-a'])
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
        res = runner.invoke(controller, ['test_chats/wa.txt', '-a', '-u', 'A'])
        expected_res = '''The user A mostly stays active around 15 Hours
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_interaction_curve_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-iC'])
        expected_res = '''The interactions in this chat have increased!
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_interaction_curve_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-iC', '-u', 'A'])
        expected_res = '''Your interactions in this chat have increased!
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


class Test_SG:
    """The main test class for Signal chat exports"""

    def test_percentage_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/sg.md', '-p'])
        expected_res = '''Signal chat recognized
Total Count: 415

For the user A
Message Count: 27
Percentage: 6.506024096385541

For the user B
Message Count: 24
Percentage: 5.783132530120482

For the user C
Message Count: 10
Percentage: 2.4096385542168677

For the user D
Message Count: 32
Percentage: 7.710843373493977

For the user E
Message Count: 35
Percentage: 8.433734939759036

For the user F
Message Count: 115
Percentage: 27.710843373493976

For the user G
Message Count: 28
Percentage: 6.746987951807229

For the user H
Message Count: 2
Percentage: 0.48192771084337355

For the user I
Message Count: 9
Percentage: 2.1686746987951806

For the user J
Message Count: 32
Percentage: 7.710843373493977

For the user K
Message Count: 70
Percentage: 16.867469879518072

For the user L
Message Count: 31
Percentage: 7.46987951807229

Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]

    def test_percentage_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/sg.md', '-p', '-u', 'A'])
        expected_res = '''Signal chat recognized
Total Count: 415

Message Count: 27
Percentage: 6.506024096385541
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_conv_starters_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/sg.md', '-cS'])
        expected_res = '''Signal chat recognized
The user F started consversation 4 time(s)
The user D started consversation 2 time(s)
The user E started consversation 2 time(s)
The user B started consversation 1 time(s)
The user A started consversation 1 time(s)
The user K started consversation 2 time(s)
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_conv_starters_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/sg.md', '-cS', '-u', 'A'])
        expected_res = '''Signal chat recognized
The user A started consversation 1 time(s)
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_activity_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/sg.md', '-a'])
        expected_res = '''Signal chat recognized
The user A mostly stays active around 13 Hours
The user B mostly stays active around 13 Hours
The user C mostly stays active around 20 Hours
The user D mostly stays active around 14 Hours
The user E mostly stays active around 14 Hours
The user F mostly stays active around 13 Hours
The user G mostly stays active around 20 Hours
The user H mostly stays active around 13 Hours
The user I mostly stays active around 13 Hours
The user J mostly stays active around 23 Hours
The user K mostly stays active around 20 Hours
The user L mostly stays active around 23 Hours
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_activity_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/sg.md', '-a', '-u', 'A'])
        expected_res = '''Signal chat recognized
The user A mostly stays active around 13 Hours
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_interaction_curve_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/sg.md', '-iC'])
        expected_res = '''Signal chat recognized
The interactions in this chat have increased!
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_interaction_curve_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/sg.md', '-iC', '-u', 'A'])
        expected_res = '''Signal chat recognized
Your interactions in this chat have increased!
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]
