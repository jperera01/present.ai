# Present.ai backend

## Starting backend

1. Install python packages

```bash
pipenv shell
pipenv install
```

2. Install pnpm packages

```bash
pnpm install
```

3. Start backend

```bash
python run.py
```
4. Start tailwind process
```bash
pnpm runtailwind
```

## File structure

. <br>
|-- Pipfile<br>
|-- Pipfile.lock<br>
|-- app (all source code)<br>
| |-- \_\_init\_\_.py (create app)<br>
| |-- config.py (flask configurations)<br>
| |-- static (store static files)<br>
| \`-- templates (store all templates)<br>
|-- node_modules<br>
|-- package.json<br>
|-- pnpm-lock.yaml<br>
|-- readme.md<br>
|-- run.py (run app)<br>
\`-- tailwind.config.js<br>
