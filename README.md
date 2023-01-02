# Multiagent-based Modelling and Simulation

## Install Python with asdf and dependencies

Use [asdf](https://asdf-vm.com/#/), with the [python plugin](https://github.com/danhper/asdf-python) to install and set the Python version.

Install Python

```
asdf install
```

Install dependencies

```
pip install -r requirements.txt
```

## Run simulation

```
python src/SimulationEngine.py
```

(ideally we would like to pass the config file as a param, for instance: `python src/SimulationEngine.py src/ant-colony.json`)
