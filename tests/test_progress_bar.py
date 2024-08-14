from typing import Any

from pytest import CaptureFixture

from progress_bar.bar import ProgressBar

Capsys = CaptureFixture[Any]


def test_bar_shows_correct_number(capsys: Capsys) -> None:
    total = 20
    p = ProgressBar(total)
    for i in range(1, 5):
        p.update(i)
        out = capsys.readouterr().out
        assert f"{i}/{total}" in out


def test_bar_prefix(capsys: Capsys) -> None:
    prefix = "hello"
    p = ProgressBar(10, bar_prefix=prefix)
    p.update(1)
    assert prefix in capsys.readouterr().out


def test_is_interactive(capsys: Capsys) -> None:
    p = ProgressBar(10)
    outs = []
    for i in range(5):
        p.update(i + 1)
        outs.append(capsys.readouterr().out)

    # make sure no newline is written, i.e. the bar stays on the same line when updated
    assert "\n" not in "".join(outs)


def test_update_with_finished(capsys: Capsys) -> None:
    p = ProgressBar(10)
    p.update(10, finished=True)
    assert "\n" in capsys.readouterr().out


def test_update_with_info_dict(capsys: Capsys) -> None:
    p = ProgressBar(1)
    info = {"test1": 123, "test2": 123}
    p.update(1, info=info)
    assert p.create_bar_info(info) in capsys.readouterr().out


def test_update_with_info_kwargs(capsys: Capsys) -> None:
    p = ProgressBar(1)
    kwargs = {"hello": 123}
    p.update(1, **kwargs)  # type: ignore
    assert p.create_bar_info(kwargs) in capsys.readouterr().out


def test_create_bar_info(capsys: Capsys) -> None:
    info = {"test1": 123, "test2": 123}
    bar_info = ProgressBar.create_bar_info(info)
    assert bar_info == "test1: 123, test2: 123"
