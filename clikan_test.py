#!/usr/bin/env python

from click.testing import CliRunner
from clikan import clikan, show
import os
import pathlib
import tempfile
LONG_STRING = 'This is a long task name, more than 40 characters (66 to be exact)'


# Configure Tests
def test_command_help():
    runner = CliRunner()
    result = runner.invoke(clikan, ['--help'])
    assert result.exit_code == 0
    assert 'Usage: clikan [OPTIONS] COMMAND [ARGS]...' in result.output
    assert 'clikan: CLI personal kanban' in result.output


def test_command_version():
    version_file = open(os.path.join('./', 'VERSION'))
    version = version_file.read().strip()

    runner = CliRunner()
    result = runner.invoke(clikan, ['--version'])
    assert result.exit_code == 0
    assert 'clikan, version {}'.format(version) in result.output


def test_command_configure(tmp_path):
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdirname:
        with runner.isolation(
            input=None,
            env={'CLIKAN_HOME': tmpdirname},
            color=False
        ):
            result = runner.invoke(clikan, ['configure'])
            assert result.exit_code == 0
            assert 'Creating' in result.output


def test_command_configure_existing():
    runner = CliRunner()
    with runner.isolated_filesystem():
        runner.invoke(clikan, ['configure'])
        result = runner.invoke(clikan, ['configure'])

        assert 'Config file exists' in result.output


# New Tests
def test_command_a():
    runner = CliRunner()
    result = runner.invoke(clikan, ['a', 'n_--task_test'])
    assert result.exit_code == 0
    assert 'n_--task_test' in result.output


# Show Tests
def test_no_command():
    runner = CliRunner()
    result = runner.invoke(clikan, [])
    assert result.exit_code == 0
    assert 'n_--task_test' in result.output


def test_command_s():
    runner = CliRunner()
    result = runner.invoke(clikan, ['s'])
    assert result.exit_code == 0
    assert 'n_--task_test' in result.output


def test_command_show():
    runner = CliRunner()
    result = runner.invoke(show)
    assert result.exit_code == 0
    assert 'n_--task_test' in result.output


def test_command_not_show():
    runner = CliRunner()
    result = runner.invoke(show)
    assert result.exit_code == 0
    assert 'blahdyblah' not in result.output


# Promote Tests
def test_command_promote():
    runner = CliRunner()
    result = runner.invoke(clikan, ['promote', '1'])
    assert result.exit_code == 0
    assert 'Promoting task 1 to in-progress.' in result.output
    result = runner.invoke(clikan, ['promote', '1'])
    assert result.exit_code == 0
    assert 'Promoting task 1 to done.' in result.output


# Delete Tests
def test_command_delete():
    runner = CliRunner()
    result = runner.invoke(clikan, ['delete', '1'])
    assert result.exit_code == 0
    assert 'Removed task 1.' in result.output
    result = runner.invoke(clikan, ['delete', '1'])
    assert result.exit_code == 0
    assert 'No existing task with' in result.output


# Repaint Tests
def test_repaint_config_option():
    runner = CliRunner()
    version_file = open(os.path.join('./', 'VERSION'))
    version = version_file.read().strip()
    path_to_config = str(pathlib.Path('./tests/repaint').resolve())
    with runner.isolation(
        input=None,
        env={'CLIKAN_HOME': path_to_config},
        color=False
    ):
        result = runner.invoke(clikan, [])
        assert result.exit_code == 0
        assert 'clikan' in result.output
        result = runner.invoke(clikan, ['a', 'n_--task_test'])
        assert result.exit_code == 0
        assert 'n_--task_test' in result.output
        assert version in result.output


def test_no_repaint_config_option():
    runner = CliRunner()
    version_file = open(os.path.join('./', 'VERSION'))
    version = version_file.read().strip()
    path_to_config = str(pathlib.Path('./tests/no_repaint').resolve())
    with runner.isolation(
        input=None,
        env={'CLIKAN_HOME': path_to_config},
        color=False
    ):
        result = runner.invoke(clikan, [])
        assert result.exit_code == 0
        assert 'clikan' in result.output
        result = runner.invoke(clikan, ['a', 'n_--task_test'])
        assert result.exit_code == 0
        assert 'n_--task_test' in result.output
        assert version not in result.output


# Limit on task name length tests
def test_taskname_config_option():
    runner = CliRunner()
    path_to_config = str(pathlib.Path('./tests/taskname').resolve())
    with runner.isolation(
        input=None,
        env={'CLIKAN_HOME': path_to_config},
        color=False
    ):
        result = runner.invoke(clikan, [])
        assert result.exit_code == 0
        assert 'clikan' in result.output
        result = runner.invoke(clikan, ['a', LONG_STRING])
        assert result.exit_code == 0
        assert LONG_STRING in result.output


def test_no_taskname_config_option():
    runner = CliRunner()
    path_to_config = str(pathlib.Path('./tests/no_taskname').resolve())
    with runner.isolation(
        input=None,
        env={'CLIKAN_HOME': path_to_config},
        color=False
    ):
        result = runner.invoke(clikan, [])
        assert result.exit_code == 0
        assert 'clikan' in result.output
        result = runner.invoke(clikan, ['a', LONG_STRING])
        assert result.exit_code == 0
        assert 'Brevity counts.' in result.output
