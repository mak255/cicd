# cicd (example CI/CD scaffold)

Small example repository that demonstrates a pluggable CI/CD scaffold with
builders, deployers and per-service configuration.

## Creating New Builders

Add a new builder in ONE file (no other changes needed):

```python
# builders/mybuilder.py
from .core import Builder, BuilderType, register_builder

# 1. Add enum value
BuilderType.MYBUILDER = auto()  # auto-generates next enum value

# 2. Create builder class
class MyBuilder(Builder):
    def build(self) -> None:
        print("building...")  # replace with real build logic

# 3. Register it
register_builder(BuilderType.MYBUILDER, MyBuilder)
```

Use it:
```python
from builders import BuilderFactory, BuilderType
builder = BuilderFactory.get_builder(BuilderType.MYBUILDER)
builder.build()
```

That's it! The plugin system auto-discovers builders.

## Project Structure

- `builders/` - builder plugins and core types
  - `core.py` - base types and plugin registry
  - `docker.py`, `bake.py`, etc - concrete builders
- `deployment.py` - deployer backends and factory
- `service.py` - service configuration models
- `program.py` - example using builders/deployers

## Quickstart

1. Copy example services config:
```bash
cp services.json.example services.json
```

2. Run example program:
```bash
python program.py
```

## Development

Install deps and run tests:
```bash
pip install -r requirements.txt
pytest -q
```

## Notes

- Replace prints with real build logic (kubectl/helm/etc)
- Add linting (black/flake8) and type checks (mypy)
