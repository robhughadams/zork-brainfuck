#!/usr/bin/env python3
"""Differential end-to-end tests for vendored zork across pipeline stages."""

from dataclasses import dataclass
import os
import pathlib
import selectors
import subprocess

import pytest

from conftest import ROOT, PYTHON, PREPROCESS, TRANSPILE


BF_INTERP = 'beef'
ZORK_PY = ROOT / 'vendor/zork-py/zork.py'
ZORK_PRE = ROOT / 'zork.pre.py'
ZORK_BF = ROOT / 'zork.bf'
PROMPTS = ('What do you do? ', 'Do you want to continue? Y/N ')


@dataclass(frozen=True)
class Scenario:
    name: str
    branch_ids: tuple[str, ...]
    inputs: tuple[str, ...]


SCENARIOS = [
    Scenario('open field take mailbox', ('field_take_mailbox', 'field_to_forest', 'forest_to_clearing', 'clearing_to_cave', 'cave_descend_staircase', 'final_open_trunk', 'final_exit_no'), ('take mailbox\n', 'go southwest\n', 'go east\n', 'descend grating\n', 'descend staircase\n', 'open trunk\n', 'n\n')),
    Scenario('open field open mailbox', ('field_open_mailbox', 'field_to_forest', 'forest_to_clearing', 'clearing_to_cave', 'cave_descend_staircase', 'final_open_trunk', 'final_exit_no'), ('open mailbox\n', 'go southwest\n', 'go east\n', 'descend grating\n', 'descend staircase\n', 'open trunk\n', 'n\n')),
    Scenario('open field go east', ('field_go_east', 'field_to_forest', 'forest_to_clearing', 'clearing_to_cave', 'cave_descend_staircase', 'final_open_trunk', 'final_exit_no'), ('go east\n', 'go southwest\n', 'go east\n', 'descend grating\n', 'descend staircase\n', 'open trunk\n', 'n\n')),
    Scenario('open field open door', ('field_open_door', 'field_to_forest', 'forest_to_clearing', 'clearing_to_cave', 'cave_descend_staircase', 'final_open_trunk', 'final_exit_no'), ('open door\n', 'go southwest\n', 'go east\n', 'descend grating\n', 'descend staircase\n', 'open trunk\n', 'n\n')),
    Scenario('open field take boards', ('field_take_boards', 'field_to_forest', 'forest_to_clearing', 'clearing_to_cave', 'cave_descend_staircase', 'final_open_trunk', 'final_exit_no'), ('take boards\n', 'go southwest\n', 'go east\n', 'descend grating\n', 'descend staircase\n', 'open trunk\n', 'n\n')),
    Scenario('open field look at house', ('field_look_house', 'field_to_forest', 'forest_to_clearing', 'clearing_to_cave', 'cave_descend_staircase', 'final_open_trunk', 'final_exit_no'), ('look at house\n', 'go southwest\n', 'go east\n', 'descend grating\n', 'descend staircase\n', 'open trunk\n', 'n\n')),
    Scenario('open field read leaflet mixed case', ('field_read_leaflet_casefold', 'field_to_forest', 'forest_to_clearing', 'clearing_to_cave', 'cave_descend_staircase', 'final_open_trunk', 'final_exit_no'), ('ReAd LeAfLeT\n', 'go southwest\n', 'go east\n', 'descend grating\n', 'descend staircase\n', 'open trunk\n', 'n\n')),
    Scenario('open field invalid command', ('field_invalid', 'field_to_forest', 'forest_to_clearing', 'clearing_to_cave', 'cave_descend_staircase', 'final_open_trunk', 'final_exit_no'), ('dance\n', 'go southwest\n', 'go east\n', 'descend grating\n', 'descend staircase\n', 'open trunk\n', 'n\n')),
    Scenario(
        'forest branches and transition',
        ('field_to_forest', 'forest_go_west', 'forest_go_north', 'forest_go_south', 'forest_invalid', 'forest_to_clearing', 'clearing_to_cave', 'cave_descend_staircase', 'final_open_trunk', 'final_exit_no'),
        ('go southwest\n', 'go west\n', 'go north\n', 'go south\n', 'sing\n', 'go east\n', 'descend grating\n', 'descend staircase\n', 'open trunk\n', 'n\n'),
    ),
    Scenario(
        'clearing branches and transition',
        ('field_to_forest', 'forest_to_clearing', 'clearing_go_south', 'clearing_invalid', 'clearing_to_cave', 'cave_descend_staircase', 'final_open_trunk', 'final_exit_no'),
        ('go southwest\n', 'go east\n', 'go south\n', 'wait\n', 'descend grating\n', 'descend staircase\n', 'open trunk\n', 'n\n'),
    ),
    Scenario(
        'cave response branches and descend staircase',
        (
            'field_to_forest',
            'forest_to_clearing',
            'clearing_to_cave',
            'cave_take_skeleton',
            'cave_smash_skeleton',
            'cave_light_up_room',
            'cave_break_skeleton',
            'cave_invalid',
            'cave_descend_staircase',
            'final_open_trunk',
            'final_exit_no',
        ),
        (
            'go southwest\n',
            'go east\n',
            'descend grating\n',
            'take skeleton\n',
            'smash skeleton\n',
            'light up room\n',
            'break skeleton\n',
            'shrug\n',
            'descend staircase\n',
            'open trunk\n',
            'n\n',
        ),
    ),
    Scenario(
        'cave alternate transitions',
        ('field_to_forest', 'forest_to_clearing', 'clearing_to_cave', 'cave_go_down_staircase', 'final_open_trunk', 'final_exit_no'),
        ('go southwest\n', 'go east\n', 'descend grating\n', 'go down staircase\n', 'open trunk\n', 'n\n'),
    ),
    Scenario(
        'cave scale staircase mixed case',
        ('field_to_forest', 'forest_to_clearing', 'clearing_to_cave', 'cave_scale_staircase', 'final_open_trunk', 'final_exit_no'),
        ('go southwest\n', 'go east\n', 'descend grating\n', 'ScAlE StAiRcAsE\n', 'open trunk\n', 'n\n'),
    ),
    Scenario(
        'suicide exit no',
        ('field_to_forest', 'forest_to_clearing', 'clearing_to_cave', 'cave_suicide', 'suicide_exit_no'),
        ('go southwest\n', 'go east\n', 'descend grating\n', 'suicide\n', 'n\n'),
    ),
    Scenario(
        'suicide restart then finish',
        (
            'field_to_forest',
            'forest_to_clearing',
            'clearing_to_cave',
            'cave_suicide',
            'suicide_restart_yes',
            'restart_to_forest',
            'restart_to_clearing',
            'restart_to_cave',
            'restart_to_final',
            'final_open_trunk',
            'final_exit_no',
        ),
        ('go southwest\n', 'go east\n', 'descend grating\n', 'suicide\n', 'y\n', 'go southwest\n', 'go east\n', 'descend grating\n', 'descend staircase\n', 'open trunk\n', 'n\n'),
    ),
    Scenario(
        'final invalid exit no',
        ('field_to_forest', 'forest_to_clearing', 'clearing_to_cave', 'cave_descend_staircase', 'final_invalid', 'final_exit_no'),
        ('go southwest\n', 'go east\n', 'descend grating\n', 'descend staircase\n', 'kick trunk\n', 'n\n'),
    ),
    Scenario(
        'final restart yes then exit no',
        (
            'field_to_forest',
            'forest_to_clearing',
            'clearing_to_cave',
            'cave_descend_staircase',
            'final_open_trunk',
            'final_restart_yes',
            'restart_to_forest',
            'restart_to_clearing',
            'restart_to_cave',
            'restart_to_final',
            'final_open_trunk',
            'final_exit_no',
        ),
        ('go southwest\n', 'go east\n', 'descend grating\n', 'descend staircase\n', 'open trunk\n', 'y\n', 'go southwest\n', 'go east\n', 'descend grating\n', 'descend staircase\n', 'open trunk\n', 'n\n'),
    ),
]

EXPECTED_BRANCHES = {
    'cave_break_skeleton',
    'cave_descend_staircase',
    'cave_go_down_staircase',
    'cave_invalid',
    'cave_light_up_room',
    'cave_scale_staircase',
    'cave_smash_skeleton',
    'cave_suicide',
    'cave_take_skeleton',
    'clearing_go_south',
    'clearing_invalid',
    'clearing_to_cave',
    'field_go_east',
    'field_invalid',
    'field_look_house',
    'field_open_door',
    'field_open_mailbox',
    'field_read_leaflet_casefold',
    'field_take_boards',
    'field_take_mailbox',
    'field_to_forest',
    'final_exit_no',
    'final_invalid',
    'final_open_trunk',
    'final_restart_yes',
    'forest_go_north',
    'forest_go_south',
    'forest_go_west',
    'forest_invalid',
    'forest_to_clearing',
    'restart_to_cave',
    'restart_to_clearing',
    'restart_to_final',
    'restart_to_forest',
    'suicide_exit_no',
    'suicide_restart_yes',
}


def preprocess_zork(output_path=ZORK_PRE):
    result = subprocess.run(
        [PYTHON, PREPROCESS, str(ZORK_PY), '--verify', '-o', str(output_path)],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    return output_path


def transpile_zork(source_path=ZORK_PRE, output_path=ZORK_BF):
    source = source_path.read_text()
    result = subprocess.run(
        [PYTHON, TRANSPILE],
        input=source,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    output_path.write_text(result.stdout)
    return output_path


def start_python_game(script_path: pathlib.Path):
    return subprocess.Popen(
        [PYTHON, '-u', str(script_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def start_bf_game(bf_path: pathlib.Path):
    return subprocess.Popen(
        [BF_INTERP, str(bf_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def read_until_prompt_or_exit(proc: subprocess.Popen, timeout: float = 10.0):
    selector = selectors.DefaultSelector()
    selector.register(proc.stdout, selectors.EVENT_READ)
    output = []
    try:
        while True:
            if proc.poll() is not None and not selector.select(timeout=0):
                break
            ready = selector.select(timeout)
            if not ready:
                raise AssertionError(f'process timed out waiting for prompt: {proc.args}')
            chunk = os.read(proc.stdout.fileno(), 1)
            if not chunk:
                break
            output.append(chunk.decode())
            if ''.join(output).endswith(PROMPTS):
                break
    finally:
        selector.close()
    return ''.join(output)


def collect_remaining(proc: subprocess.Popen):
    stdout, stderr = proc.communicate(timeout=10)
    return stdout.decode(), stderr.decode(), proc.returncode


def run_lockstep(proc_a: subprocess.Popen, proc_b: subprocess.Popen, scenario: Scenario, label_a: str, label_b: str):
    initial_a = read_until_prompt_or_exit(proc_a)
    initial_b = read_until_prompt_or_exit(proc_b)
    assert initial_a == initial_b, format_diff(scenario.name, 0, label_a, initial_a, label_b, initial_b)

    for turn, user_input in enumerate(scenario.inputs, start=1):
        proc_a.stdin.write(user_input.encode())
        proc_a.stdin.flush()
        proc_b.stdin.write(user_input.encode())
        proc_b.stdin.flush()

        chunk_a = read_until_prompt_or_exit(proc_a)
        chunk_b = read_until_prompt_or_exit(proc_b)
        assert chunk_a == chunk_b, format_diff(scenario.name, turn, label_a, chunk_a, label_b, chunk_b, user_input)

    tail_a, err_a, code_a = collect_remaining(proc_a)
    tail_b, err_b, code_b = collect_remaining(proc_b)

    assert tail_a == tail_b, format_diff(scenario.name, len(scenario.inputs) + 1, label_a, tail_a, label_b, tail_b)
    assert err_a == err_b, format_stream_diff(scenario.name, label_a, err_a, label_b, err_b, 'stderr')
    assert code_a == code_b, f'{scenario.name}: return code mismatch {label_a}={code_a} {label_b}={code_b}'


def format_diff(scenario_name, turn, label_a, output_a, label_b, output_b, user_input=None):
    lines = [f'{scenario_name}: divergence at turn {turn}']
    if user_input is not None:
        lines.append(f'input: {user_input!r}')
    lines.append(f'{label_a}: {output_a!r}')
    lines.append(f'{label_b}: {output_b!r}')
    return '\n'.join(lines)


def format_stream_diff(scenario_name, label_a, output_a, label_b, output_b, stream_name):
    return '\n'.join(
        [
            f'{scenario_name}: {stream_name} mismatch',
            f'{label_a}: {output_a!r}',
            f'{label_b}: {output_b!r}',
        ]
    )


@pytest.fixture(scope='module')
def built_zork_artifacts():
    pre_path = preprocess_zork()
    bf_path = transpile_zork(pre_path)
    return pre_path, bf_path


class TestZorkDifferentialE2E:
    def test_manifest_covers_all_declared_branches(self):
        covered = {branch_id for scenario in SCENARIOS for branch_id in scenario.branch_ids}
        assert covered == EXPECTED_BRANCHES

    @pytest.mark.parametrize('scenario', SCENARIOS, ids=lambda scenario: scenario.name)
    def test_original_matches_lowered_python(self, scenario, built_zork_artifacts):
        pre_path, _ = built_zork_artifacts
        proc_original = start_python_game(ZORK_PY)
        proc_lowered = start_python_game(pre_path)
        try:
            run_lockstep(proc_original, proc_lowered, scenario, 'original', 'lowered')
        finally:
            if proc_original.poll() is None:
                proc_original.kill()
                proc_original.wait(timeout=5)
            if proc_lowered.poll() is None:
                proc_lowered.kill()
                proc_lowered.wait(timeout=5)

    @pytest.mark.parametrize('scenario', SCENARIOS, ids=lambda scenario: scenario.name)
    def test_lowered_python_matches_bf(self, scenario, built_zork_artifacts):
        pre_path, bf_path = built_zork_artifacts
        proc_lowered = start_python_game(pre_path)
        proc_bf = start_bf_game(bf_path)
        try:
            run_lockstep(proc_lowered, proc_bf, scenario, 'lowered', 'bf')
        finally:
            if proc_lowered.poll() is None:
                proc_lowered.kill()
                proc_lowered.wait(timeout=5)
            if proc_bf.poll() is None:
                proc_bf.kill()
                proc_bf.wait(timeout=5)
