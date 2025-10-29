# Dynamic Ocean Fields Environment

Grid-based ocean routing environment for Prime Intellect Hub.

## Usage

```python
from load_environment import load_environment
env_factory = load_environment()
env = env_factory()
obs, info = env.reset()
```
