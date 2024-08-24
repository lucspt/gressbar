Hey, this is a simple progress bar package, similar to `tqdm`. Here's how it works

```python
import time
from gressbar import ProgressBar

# specify a "total" of 10. Progress will be assumed complete at the 10th step.
p = ProgressBar(10)

for step in range(1, 11):
  p.update(step)
  time.sleep(0.1)
```

This will write to stdout an interactive progress bar that looks like:

1/10 <span style="color: green;">━━</span>━━━━━━━━━━━━━━━━━━

With the step number changing each iteration.

You can also add information to the right of the bar:

```python
import time
from gressbar import ProgressBar

p = ProgressBar(10)

for step in range(1, 11):
  p.update(step, info={"step num": step}, step=step, hello="world")
  time.sleep(0.1)
```

Keyword arguments or a `info` dictionary is accepted. Keyword arguments will take precendence over the `info` dictionary.

This will output:

9/10 <span style="color: green;">━━━━━━━━━━━━━━━━━━</span>━━ step num: 9, step: 9, hello: world

Check out the [`ProgressBar`](./reference/bar.md) for more!
