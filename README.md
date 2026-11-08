# Transport in Europe: Motorisation and Emissions

Group project for PRF at ISEG, 2026/27.

## Setup

You need **Python 3.10+**, **Git** and **VS Code** (with the Python and Jupyter extensions).

```bash
git clone https://github.com/Adrianhammer/PRF_Project.git
cd PRF_Project
./start.sh
```

`start.sh` creates the virtual environment (first time only), installs the packages
and starts the app at <http://127.0.0.1:5000>. Stop it with **Ctrl+C**.

<details>
<summary>Doing it manually instead</summary>

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd app
flask --app app run --debug
```
</details>

## Notebook

Open `notebooks/transport_emissions.ipynb` in VS Code, choose **Select Kernel → .venv**,
and click **Run All**. The last cell saves the data to `data/processed/panel.csv`,
which the app reads. Commit that file when it changes.

## Adding a package

Add it to `requirements.txt` and commit. The next `./start.sh` installs it.
