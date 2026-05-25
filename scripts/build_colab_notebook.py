"""Gera fooocus_colab.ipynb — executar localmente: python scripts/build_colab_notebook.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "fooocus_colab.ipynb"

cells = []

cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# Fooocus no Google Colab (com download de modelos)\n",
        "\n",
        "Clona o Fooocus, baixa checkpoints/loras/VAE dos presets (incl. SDXL NSFW/realistas) e inicia a UI.\n",
        "\n",
        "**Ordem:** Config → Clone → Download → Iniciar\n",
        "\n",
        "Ver `COLAB-MODELS.md`. Avisos: NSFW, ~40–70 GB, token Civitai pode ser necessário.\n",
    ],
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# @title Configuracao\n",
        "import os\n",
        "\n",
        "REPO_URL = \"https://github.com/lllyasviel/Fooocus.git\"  # use seu fork para presets deste repo\n",
        "REPO_BRANCH = \"main\"\n",
        "\n",
        "CIVITAI_TOKEN = os.environ.get(\"CIVITAI_TOKEN\", \"\")\n",
        "\n",
        "DOWNLOAD_ALL_PRESET_MODELS = True\n",
        "DOWNLOAD_NSFW_EXTRAS = True\n",
        "DOWNLOAD_LUSTIFY_APEX_V8 = False\n",
        "DOWNLOAD_EPIC_VX_FINALKISS = True\n",
        "DOWNLOAD_REED_V14 = False\n",
        "\n",
        "FOOOCUS_PRESET = \"default\"\n",
        "\n",
        "FOOOCUS_DIR = \"/content/Fooocus\"\n",
        "CHECKPOINT_DIR = f\"{FOOOCUS_DIR}/models/checkpoints\"\n",
        "LORA_DIR = f\"{FOOOCUS_DIR}/models/loras\"\n",
        "VAE_DIR = f\"{FOOOCUS_DIR}/models/vae\"\n",
        "\n",
        "print(\"Preset:\", FOOOCUS_PRESET)\n",
        "print(\"Civitai token:\", \"sim\" if CIVITAI_TOKEN else \"nao\")\n",
    ],
    "execution_count": None,
    "outputs": [],
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# @title 1) Clone e dependencias\n",
        "!pip install -q pygit2==1.15.1\n",
        "import os, shutil, subprocess\n",
        "os.chdir(\"/content\")\n",
        "if os.path.isdir(FOOOCUS_DIR):\n",
        "    shutil.rmtree(FOOOCUS_DIR)\n",
        "subprocess.run([\"git\", \"clone\", \"--branch\", REPO_BRANCH, \"--depth\", \"1\", REPO_URL, FOOOCUS_DIR], check=True)\n",
        "os.chdir(FOOOCUS_DIR)\n",
        "for d in [\"models/checkpoints\", \"models/loras\", \"models/vae\", \"models/embeddings\"]:\n",
        "    os.makedirs(d, exist_ok=True)\n",
        "print(\"Repo:\", os.getcwd())\n",
    ],
    "execution_count": None,
    "outputs": [],
})

download_lines = Path(__file__).with_name("_colab_download_cell.py").read_text(encoding="utf-8").splitlines(True)
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": download_lines,
    "execution_count": None,
    "outputs": [],
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# @title 3) Iniciar Fooocus\n",
        "%cd /content/Fooocus\n",
        "args = \"--share --always-high-vram\"\n",
        "if FOOOCUS_PRESET:\n",
        "    args += f\" --preset {FOOOCUS_PRESET}\"\n",
        "print(\"python entry_with_update.py\", args)\n",
        "import subprocess\n",
        "subprocess.run([\"python\", \"entry_with_update.py\"] + args.split(), check=False)\n",
    ],
    "execution_count": None,
    "outputs": [],
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# @title (Opcional) Download manual Civitai\n",
        "MANUAL_URL = \"\"\n",
        "MANUAL_FILENAME = \"\"\n",
        "if MANUAL_URL and MANUAL_FILENAME:\n",
        "    download_one(MANUAL_URL, os.path.join(CHECKPOINT_DIR, MANUAL_FILENAME), CIVITAI_TOKEN)\n",
        "else:\n",
        "    print(\"Cole MANUAL_URL (api/download/models/ID) e MANUAL_FILENAME.\")\n",
    ],
    "execution_count": None,
    "outputs": [],
})

nb = {
    "nbformat": 4,
    "nbformat_minor": 0,
    "metadata": {
        "accelerator": "GPU",
        "colab": {"gpuType": "T4", "provenance": []},
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "cells": cells,
}

OUT.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
print("Wrote", OUT)
