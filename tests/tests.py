import sys

sys.path.append("../src")

from click.testing import CliRunner

from chat_analyzer import controller


class Test_WA:
    """The main test class for Whatsapp chat exports"""

    def test_percentage_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-p'])
        expected_res = '''Total No. of Messages: 39939

╒════════════╤═════════════════╤══════════════╕
│  Username  │  Message Count  │  Percentage  │
╞════════════╪═════════════════╪══════════════╡
│     A      │      6872       │   17.2062    │
├────────────┼─────────────────┼──────────────┤
│     B      │      7012       │   17.5568    │
├────────────┼─────────────────┼──────────────┤
│     C      │      9260       │   23.1854    │
├────────────┼─────────────────┼──────────────┤
│     D      │      8518       │   21.3275    │
├────────────┼─────────────────┼──────────────┤
│     E      │      6456       │   16.1647    │
├────────────┼─────────────────┼──────────────┤
│     F      │      1776       │    4.4468    │
├────────────┼─────────────────┼──────────────┤
│     G      │       44        │    0.1102    │
├────────────┼─────────────────┼──────────────┤
│     H      │        1        │    0.0025    │
╘════════════╧═════════════════╧══════════════╛
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_percentage_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-p', '-u', 'A'])
        expected_res = '''Total No. of Messages: 39939

╒════════════╤═════════════════╤══════════════╕
│  Username  │  Message Count  │  Percentage  │
╞════════════╪═════════════════╪══════════════╡
│     A      │      6872       │   17.2062    │
╘════════════╧═════════════════╧══════════════╛
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_conv_starters_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-cS'])
        expected_res = '''The user C started conversation 255 time(s)
The user E started conversation 159 time(s)
The user A started conversation 302 time(s)
The user D started conversation 283 time(s)
The user B started conversation 187 time(s)
The user F started conversation 89 time(s)
The user G started conversation 4 time(s)
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_conv_starters_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-cS', '-u', 'A'])
        expected_res = '''The user A started conversation 302 time(s)
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
Total No. of Messages: 415

╒════════════╤═════════════════╤══════════════╕
│  Username  │  Message Count  │  Percentage  │
╞════════════╪═════════════════╪══════════════╡
│     A      │       27        │    6.5060    │
├────────────┼─────────────────┼──────────────┤
│     B      │       24        │    5.7831    │
├────────────┼─────────────────┼──────────────┤
│     C      │       10        │    2.4096    │
├────────────┼─────────────────┼──────────────┤
│     D      │       32        │    7.7108    │
├────────────┼─────────────────┼──────────────┤
│     E      │       35        │    8.4337    │
├────────────┼─────────────────┼──────────────┤
│     F      │       115       │   27.7108    │
├────────────┼─────────────────┼──────────────┤
│     G      │       28        │    6.7470    │
├────────────┼─────────────────┼──────────────┤
│     H      │        2        │    0.4819    │
├────────────┼─────────────────┼──────────────┤
│     I      │        9        │    2.1687    │
├────────────┼─────────────────┼──────────────┤
│     J      │       32        │    7.7108    │
├────────────┼─────────────────┼──────────────┤
│     K      │       70        │   16.8675    │
├────────────┼─────────────────┼──────────────┤
│     L      │       31        │    7.4699    │
╘════════════╧═════════════════╧══════════════╛
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]

    def test_percentage_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/sg.md', '-p', '-u', 'A'])
        expected_res = '''Signal chat recognized
Total No. of Messages: 415

╒════════════╤═════════════════╤══════════════╕
│  Username  │  Message Count  │  Percentage  │
╞════════════╪═════════════════╪══════════════╡
│     A      │       27        │    6.5060    │
╘════════════╧═════════════════╧══════════════╛
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_conv_starters_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/sg.md', '-cS'])
        expected_res = '''Signal chat recognized
The user F started conversation 4 time(s)
The user D started conversation 2 time(s)
The user E started conversation 2 time(s)
The user B started conversation 1 time(s)
The user A started conversation 1 time(s)
The user K started conversation 2 time(s)
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_conv_starters_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/sg.md', '-cS', '-u', 'A'])
        expected_res = '''Signal chat recognized
The user A started conversation 1 time(s)
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
