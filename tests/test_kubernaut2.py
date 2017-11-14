import pytest
import requests
import requests_mock
import pathlib2

from click.testing import CliRunner

from . import *
from kubernaut.cli import cli


def jsonify(dictionary: dict) -> str:
    import json
    return json.dumps(dictionary)


def test_set_token(tmpdir):
    runner = CliRunner(
        env={"HOME": str(tmpdir)}
    )

    result = runner.invoke(cli, ['set-token', "I_AM_THE_WALRUS"])
    config = get_config(tmpdir)

    assert config["kubernaut.io"]["token"] == "I_AM_THE_WALRUS"
    assert result.exit_code == 0


def test_get_token(tmpdir):
    runner = CliRunner(
        env={"HOME": str(tmpdir)}
    )

    result = runner.invoke(cli, ['get-token'])
    assert result.exit_code == 0


def test_claim_without_access_token_gracefully_errors(tmpdir):
    runner = CliRunner(
        env={"HOME": str(tmpdir)}
    )

    result = runner.invoke(cli, ["claim"])
    assert load_output("access_token_not_set.txt") == result.output
    assert 2 == result.exit_code


@requests_mock.Mocker(kw="mocker")
@pytest.mark.parametrize("shell", [
    "/bin/bash",
    "/bin/zsh",
    "/bin/fish",
    "/bin/csh",
    "/bin/tcsh",
])
def test_successful_claim(tmpdir, monkeypatch, shell, **kwargs):
    monkeypatch.setattr("pathlib2.Path.home", lambda: pathlib2.Path(str(tmpdir)), raising=True)

    kwargs["mocker"].post(
        'https://kubernaut.io/claims',
        text=load_output("api_successful_claim_main.json"),
        status_code=200
    )

    set_token(tmpdir, host="kubernaut.io", token="TOKEN_DOES_NOT_MATTER")

    runner = CliRunner(
        env={"HOME": str(tmpdir), "SHELL": shell}
    )

    result = runner.invoke(cli, ["claim"])
    assert result.exit_code == 0

    print(result.output)

    expected = load_output("claim_set_shell_{0}.txt".format(shell[1:].replace('/', '-')))
    expected = expected.format(str(tmpdir.join(".kube", "kubernaut")))

    assert expected == result.output

    with open(str(tmpdir.join(".kube", "kubernaut"))) as f:
        assert "KUBECONFIG_DOES_NOT_MATTER" == f.read()
