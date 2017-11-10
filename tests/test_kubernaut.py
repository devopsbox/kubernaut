from kubernaut.cli import cli
from click.testing import CliRunner
from . import *

import unittest
import os


class TestKubernaut(unittest.TestCase):

    def test_set_token(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['set-token', "I_AM_THE_WALRUS"])

        config = get_config()
        assert result.exit_code == 0
        assert config[os.environ["KUBERNAUT_HOST"]]["token"] == "I_AM_THE_WALRUS"

    def test_get_token(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['get-token'])

        assert result.exit_code == 0

    def test_claim(self):
        pass

    def test_discard(self):
        pass


