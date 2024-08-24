import sys
import math
from typing import Any, Optional


class ProgressBar:
    """An interactive progress bar that logs stdout.

    Attributes:
        target (int): The integer denoting the target at which progress is completed.
        width (int): The width of the bar. Defaults to `20`.
        bar_prefix (str, optional): An optional string to prefix the bar with.
    """

    def __init__(
        self,
        target: int,
        *,
        width: int = 20,
        bar_prefix: Optional[str] = "",
    ) -> None:
        """Initialize a progress bar.

        Args:
            target (int): The integer denoting the target at which progress is completed.
            width (int): The width of the bar. Defaults to `20`.
            bar_prefix (str, Optional): An optional string to prefix the bar with.
        """
        self.target = target
        self.width = width
        self._prev_width = 0
        self.bar_prefix = f"{bar_prefix} " if bar_prefix else ""

    @staticmethod
    def log_msg(message: str, /, *, line_break: bool = True) -> None:
        """Log a message to `stdout` and flush."""
        sys.stdout.write("".join([message, "\n"]) if line_break else message)
        sys.stdout.flush()

    @staticmethod
    def create_bar_info(info_dict: dict[str, Any]) -> str:
        """Turn a dictionary into a comma-separated string."""
        return ", ".join([f"{k}: {v}" for k, v in info_dict.items()])

    def update(
        self,
        current: int,
        *,
        info: Optional[dict[str, Any]] = None,
        indent: int = 0,
        finished: Optional[bool] = None,
        **info_kwargs: Any,
    ) -> None:
        """Perform an interactive update of the bar.

        Args:
            current (int): The bar's current progress.
            info (dict[str, Any], Optional): An optional dictionary containing info to log to the right of the bar.
            indent (int): An indent to apply to the bar. Defaults to zero.
            finished (bool, Optional): Whether or not the bar is finished.
                By default, this is true only if `current` is equal to `self.total`
            info_kwargs: keyword arguments to log to the right of the bar, any keywords conflicting with keys of `info`
                will take precendence.s
        """
        n_special_chars = 0

        numdigits = int(math.log10(self.target)) + 1
        bard = f"%{numdigits}d/%d" % (current, self.target)
        _bar = [f"\x1b[1m{bard}\x1b[0m "]

        prog = float(current) / self.target
        prog_width = int(self.width * prog)

        if prog_width > 0:
            _bar.extend(["\33[32m", "━" * prog_width, "\x1b[0m"])
            n_special_chars += 9
        _bar.extend(["\33[37m", "━" * (self.width - prog_width), "\x1b[0m"])
        bar = "".join(_bar)

        n_special_chars += 17
        message = [
            "\b" * self._prev_width,
            "\r",
            " " * indent,
            self.bar_prefix,
            bar,
        ]

        bar_info = ""

        if info or info_kwargs:
            bar_info = self.create_bar_info((info or {}) | (info_kwargs or {}))
            message.extend([" ", bar_info])

        total_width = len(bar) + len(bar_info) + 1 - n_special_chars

        if self._prev_width > total_width:
            message.append(" " * (self._prev_width - total_width))

        self._prev_width = total_width
        self.log_msg(
            "".join(message),
            line_break=current == self.target if finished is None else finished,
        )
