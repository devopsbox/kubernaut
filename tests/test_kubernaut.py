import pytest
import re
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
    monkeypatch.setattr("pathlib2.Path.home", lambda: pathlib2.Path(str(tmpdir)))

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

    expected = load_output("claim_set_shell_{0}.txt".format(shell[1:].replace('/', '-')))
    expected = expected.format(str(tmpdir.join(".kube", "kubernaut")))

    assert expected == result.output

    with open(str(tmpdir.join(".kube", "kubernaut"))) as f:
        assert "KUBECONFIG_DOES_NOT_MATTER" == f.read()


@requests_mock.Mocker(kw="mocker")
def test_cli_claim_already_exists_graceful_failure(tmpdir, monkeypatch, **kwargs):
    monkeypatch.setattr("pathlib2.Path.home", lambda: pathlib2.Path(str(tmpdir)))

    kwargs["mocker"].post(
        'https://kubernaut.io/claims',
        text=load_output("error_ClaimAlreadyExists_api.json"),
        status_code=409
    )

    set_token(tmpdir, host="kubernaut.io", token="TOKEN_DOES_NOT_MATTER")

    runner = CliRunner(env={"HOME": str(tmpdir)})
    result = runner.invoke(cli, ["claim", "--name", "duplicate"])

    assert load_output("error_ClaimAlreadyExists_cli.txt") == result.output
    assert 1 == result.exit_code


@requests_mock.Mocker(kw="mocker")
def test_cli_kubeconfig_claim_not_found_graceful_failure(tmpdir, monkeypatch, **kwargs):
    monkeypatch.setattr("pathlib2.Path.home", lambda: pathlib2.Path(str(tmpdir)))

    kwargs["mocker"].get(
        'https://kubernaut.io/claims/main',
        text=load_output("error_ClaimNotFound_api.json"),
        status_code=404
    )

    set_token(tmpdir, host="kubernaut.io", token="TOKEN_DOES_NOT_MATTER")

    runner = CliRunner(env={"HOME": str(tmpdir)})
    result = runner.invoke(cli, ["kubeconfig"])

    assert load_output("error_ClaimNotFound_cli.txt") == result.output
    assert 1 == result.exit_code


@requests_mock.Mocker(kw="mocker")
def test_cli_connection_error_graceful_failure(tmpdir, monkeypatch, **kwargs):
    monkeypatch.setattr("pathlib2.Path.home", lambda: pathlib2.Path(str(tmpdir)))

    kwargs["mocker"].get(
        'https://kubernaut.io/claims/main',
        exc=requests.exceptions.ConnectionError
    )

    set_token(tmpdir, host="kubernaut.io", token="TOKEN_DOES_NOT_MATTER")

    runner = CliRunner(env={"HOME": str(tmpdir)})
    result = runner.invoke(cli, ["kubeconfig"])

    processed_output = re.sub("[0-9A-F]{8}-[0-9A-F]{4}-[4][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}",
                              "[DYNAMIC_UUID]", result.output, flags=re.IGNORECASE)

    assert load_output("error_ConnectionError_cli.txt") == processed_output
    assert 2 == result.exit_code


@requests_mock.Mocker(kw="mocker")
def test_cli_timeout_graceful_failure(tmpdir, monkeypatch, **kwargs):
    monkeypatch.setattr("pathlib2.Path.home", lambda: pathlib2.Path(str(tmpdir)))

    kwargs["mocker"].get(
        'https://kubernaut.io/claims/main',
        exc=requests.exceptions.Timeout
    )

    set_token(tmpdir, host="kubernaut.io", token="TOKEN_DOES_NOT_MATTER")

    runner = CliRunner(env={"HOME": str(tmpdir)})
    result = runner.invoke(cli, ["kubeconfig"])

    processed_output = re.sub("[0-9A-F]{8}-[0-9A-F]{4}-[4][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}",
                              "[DYNAMIC_UUID]", result.output, flags=re.IGNORECASE)

    assert load_output("error_Timeout_cli.txt") == processed_output
    assert 2 == result.exit_code

