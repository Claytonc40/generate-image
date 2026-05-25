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
        "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]"
        "(https://colab.research.google.com/github/Claytonc40/generate-image/blob/main/fooocus_colab.ipynb)\n",
        "\n",
        "Clona o Fooocus, baixa **Lustify v4** + essenciais Fooocus e inicia a UI.\n",
        "\n",
        "**Ordem:** Config → Clone → Download → Iniciar\n",
        "\n",
        "Ver `COLAB-MODELS.md`. Avisos: NSFW, ~10–15 GB nesta célula; downloads só via HuggingFace.\n",
    ],
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# @title Configuracao\n",
        "import os\n",
        "\n",
        "REPO_URL = \"https://github.com/Claytonc40/generate-image.git\"\n",
        "REPO_BRANCH = \"main\"\n",
        "\n",
        "# Colab lustify-only (outros presets no repo não são baixados aqui)\n",
        "DOWNLOAD_ALL_PRESET_MODELS = False\n",
        "DOWNLOAD_NSFW_EXTRAS = False\n",
        "\n",
        "FOOOCUS_PRESET = \"lustify_v4\"\n",
        "\n",
        "FOOOCUS_DIR = \"/content/Fooocus\"\n",
        "CHECKPOINT_DIR = f\"{FOOOCUS_DIR}/models/checkpoints\"\n",
        "LORA_DIR = f\"{FOOOCUS_DIR}/models/loras\"\n",
        "VAE_DIR = f\"{FOOOCUS_DIR}/models/vae\"\n",
        "\n",
        "print(\"Preset:\", FOOOCUS_PRESET)\n",
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
        "import os\n",
        "\n",
        "os.chdir(FOOOCUS_DIR)\n",
        "\n",
        "# entry_with_update.py faz git fetch no origin — no Colab costuma travar\n",
        "# (sem credenciais / rede lenta) antes do Gradio subir. Clone já trouxe o repo.\n",
        "SKIP_GIT_UPDATE = True\n",
        "\n",
        "os.environ[\"PYTHONUNBUFFERED\"] = \"1\"\n",
        "os.environ.setdefault(\"GRADIO_SERVER_NAME\", \"0.0.0.0\")\n",
        "\n",
        "args = \"--share --always-high-vram --disable-in-browser --listen\"\n",
        "if FOOOCUS_PRESET:\n",
        "    args += f\" --preset {FOOOCUS_PRESET}\"\n",
        "\n",
        "entry = \"launch.py\" if SKIP_GIT_UPDATE else \"entry_with_update.py\"\n",
        "cmd = f\"python -u {entry} {args}\"\n",
        "\n",
        "print(\"Executando:\", cmd)\n",
        "print()\n",
        "print(\"=\" * 60)\n",
        "print(\"Esta célula fica rodando até você interromper (■).\")\n",
        "print(\"1) Instala deps / carrega modelos — pode levar vários minutos.\")\n",
        "print(\"2) APÓS ver 'Loading models' no log, aguarde mais 3–10 min.\")\n",
        "print(\"3) Procure no output:\")\n",
        "print('   Running on public URL: https://....gradio.live')\n",
        "print(\"   ou 'App started successful' com link *.gradio.live*\")\n",
        "print(\"=\" * 60)\n",
        "print()\n",
        "\n",
        "# subprocess com PIPE oculta o link do Gradio; shell herda stdout/stderr\n",
        "get_ipython().system(cmd)\n",
    ],
    "execution_count": None,
    "outputs": [],
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# @title (Opcional) Download manual (HF ou URL direta)\n",
        "MANUAL_URL = \"\"\n",
        "MANUAL_FILENAME = \"\"\n",
        "if MANUAL_URL and MANUAL_FILENAME:\n",
        "    download_one(MANUAL_URL, os.path.join(CHECKPOINT_DIR, MANUAL_FILENAME))\n",
        "else:\n",
        "    print(\"Cole MANUAL_URL (resolve/main/...) e MANUAL_FILENAME.\")\n",
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
