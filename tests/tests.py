import sys

sys.path.append("../src")

from click.testing import CliRunner

from chat_analyzer import controller


class Test_WA:
    """The main test class for Whatsapp chat exports"""

    def test_percentage_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-p'])
        expected_res = '''Whatsapp chat recognized
Total No. of Messages: 39939

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
        expected_res = '''Whatsapp chat recognized
Total No. of Messages: 39939

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
        expected_res = '''Whatsapp chat recognized
╒════════╤═════════╕
│  User  │  Count  │
╞════════╪═════════╡
│   C    │   255   │
├────────┼─────────┤
│   E    │   159   │
├────────┼─────────┤
│   A    │   302   │
├────────┼─────────┤
│   D    │   283   │
├────────┼─────────┤
│   B    │   187   │
├────────┼─────────┤
│   F    │   89    │
├────────┼─────────┤
│   G    │    4    │
╘════════╧═════════╛
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_conv_starters_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-cS', '-u', 'A'])
        expected_res = '''Whatsapp chat recognized
╒════════╤═════════╕
│  User  │  Count  │
╞════════╪═════════╡
│   A    │   302   │
╘════════╧═════════╛
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_activity_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-a'])
        expected_res = '''Whatsapp chat recognized
╒════════╤════════════════╕
│  User  │  Hours Active  │
╞════════╪════════════════╡
│   A    │       15       │
├────────┼────────────────┤
│   B    │       15       │
├────────┼────────────────┤
│   C    │       15       │
├────────┼────────────────┤
│   D    │       15       │
├────────┼────────────────┤
│   E    │       15       │
├────────┼────────────────┤
│   F    │       14       │
├────────┼────────────────┤
│   G    │       18       │
├────────┼────────────────┤
│   H    │       21       │
╘════════╧════════════════╛
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_activity_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-a', '-u', 'A'])
        expected_res = '''Whatsapp chat recognized
The user A mostly stays active around 15 Hours
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_interaction_curve_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-iC'])
        expected_res = '''Whatsapp chat recognized
The interactions in this chat have increased!
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_interaction_curve_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/wa.txt', '-iC', '-u', 'A'])
        expected_res = '''Whatsapp chat recognized
Your interactions in this chat have increased!
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
╒════════╤═════════╕
│  User  │  Count  │
╞════════╪═════════╡
│   F    │    4    │
├────────┼─────────┤
│   D    │    2    │
├────────┼─────────┤
│   E    │    2    │
├────────┼─────────┤
│   B    │    1    │
├────────┼─────────┤
│   A    │    1    │
├────────┼─────────┤
│   K    │    2    │
╘════════╧═════════╛
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_conv_starters_user(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/sg.md', '-cS', '-u', 'A'])
        expected_res = '''Signal chat recognized
╒════════╤═════════╕
│  User  │  Count  │
╞════════╪═════════╡
│   A    │    1    │
╘════════╧═════════╛
Program Finished'''
        assert expected_res == res.output[:res.output[:-1].rfind('\n')]


    def test_activity_all(self):
        runner = CliRunner()
        res = runner.invoke(controller, ['test_chats/sg.md', '-a'])
        expected_res = '''Signal chat recognized
╒════════╤════════════════╕
│  User  │  Hours Active  │
╞════════╪════════════════╡
│   A    │       13       │
├────────┼────────────────┤
│   B    │       13       │
├────────┼────────────────┤
│   C    │       20       │
├────────┼────────────────┤
│   D    │       14       │
├────────┼────────────────┤
│   E    │       14       │
├────────┼────────────────┤
│   F    │       13       │
├────────┼────────────────┤
│   G    │       20       │
├────────┼────────────────┤
│   H    │       13       │
├────────┼────────────────┤
│   I    │       13       │
├────────┼────────────────┤
│   J    │       23       │
├────────┼────────────────┤
│   K    │       20       │
├────────┼────────────────┤
│   L    │       23       │
╘════════╧════════════════╛
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
