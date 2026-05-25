# Fooocus no Google Colab — modelos e downloads (Lustify v4)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Claytonc40/generate-image/blob/main/fooocus_colab.ipynb)

Guia em português para o notebook `fooocus_colab.ipynb` no repositório [Claytonc40/generate-image](https://github.com/Claytonc40/generate-image): download mínimo para disco Colab (~114 GB), preset **lustify_v4** e URLs **apenas HuggingFace**.

## Ordem de execução no Colab

| Passo | Célula | O que faz |
|-------|--------|-----------|
| 1 | **Configuração** | `FOOOCUS_PRESET = "lustify_v4"`; flags extras desligadas |
| 2 | **Clone** | `git clone` → `/content/Fooocus`, cria pastas `models/` |
| 3 | **Download** | Lustify v4 + vae_approx + prompt expansion (HF) |
| 4 | **Iniciar** | `python -u launch.py --share --always-high-vram --listen --preset lustify_v4` (sem git fetch) |
| 5 | *(opcional)* | Upload manual de outros checkpoints (não baixados por padrão) |

**Runtime:** GPU (T4 ou superior). **Disco desta célula:** ~10–15 GB (checkpoint ~6,7 GB + essenciais ~0,5–1 GB). PyTorch/deps e modelos sob demanda (controlnet, inpaint, IP-Adapter) somam mais se você usar esses recursos na UI.

## Avisos importantes

- **Conteúdo NSFW:** Lustify é explícito. Use apenas onde for legal e permitido.
- **Colab lustify-only:** pony, juggernaut, anteros, reed, epic, realisticStockPhoto, etc. **não** são baixados pela célula 2. Os ficheiros `presets/*.json` podem existir no clone do repo; o download ignora todos exceto `lustify_v4.json`.
- **Sessão Colab:** arquivos em `/content` somem ao desligar a sessão.
- **Sem Civitai:** o fluxo principal **não** usa URLs `civitai.com`.
- **Repositório:** clone padrão `https://github.com/Claytonc40/generate-image.git` (branch `main`).

## O que a célula 2 baixa agora

| Tipo | Arquivo | URL HuggingFace | Tamanho aprox. |
|------|---------|-----------------|----------------|
| Checkpoint | lustifySDXLNSFW_v40Alpha.safetensors | https://huggingface.co/xxxpo13/LUSTIFY_SDXL/resolve/main/lustifySDXLNSFWSFW_v40.safetensors | ~6,7 GB |
| VAE approx | xlvaeapp.pth | https://huggingface.co/lllyasviel/misc/resolve/main/xlvaeapp.pth | pequeno |
| VAE approx | vaeapp_sd15.pt | https://huggingface.co/lllyasviel/misc/resolve/main/vaeapp_sd15.pt | pequeno |
| VAE approx | xl-to-v1_interposer-v4.0.safetensors | https://huggingface.co/mashb1t/misc/resolve/main/xl-to-v1_interposer-v4.0.safetensors | pequeno |
| Prompt expansion | pytorch_model.bin (fooocus_expansion) | https://huggingface.co/lllyasviel/misc/resolve/main/fooocus_expansion.bin | pequeno |

**Nota:** o ficheiro no HF chama-se `lustifySDXLNSFWSFW_v40.safetensors`; no Colab é guardado como `lustifySDXLNSFW_v40Alpha.safetensors` (preset `lustify_v4`).

**Não baixados por padrão:** LoRAs do preset default (`sd_xl_offset`), Pony VAE, pacote NSFW de 6 modelos, REED, Lustify APEX, epic vxFinalkiss, etc.

## Preset lustify_v4 na UI

1. Abra o link `gradio.live` gerado pelo Colab.
2. O preset inicial é **lustify_v4** (`FOOOCUS_PRESET`).
3. Em **Model**, deve aparecer `lustifySDXLNSFW_v40Alpha.safetensors`.

Outros presets listados no menu vêm dos JSON no repo clonado, mas **sem checkpoint correspondente** até upload manual.

## Downloads sob demanda (primeira utilização na UI)

O `launch.py` / Fooocus pode baixar quando você usa o recurso:

- ControlNet (canny, CPDS)
- Inpaint (v1 / v2.5 / v2.6)
- IP-Adapter, upscale, SAM, loras de performance (LCM, Lightning, …)

Isso é independente da célula 2 e pode aumentar o uso de disco além dos ~10–15 GB base.

## Download manual (célula opcional)

```python
MANUAL_URL = "https://huggingface.co/SEU_REPO/resolve/main/modelo.safetensors"
MANUAL_FILENAME = "nome_do_arquivo.safetensors"
```

```bash
wget -c -O /content/Fooocus/models/checkpoints/modelo.safetensors \
  "https://huggingface.co/REPO/resolve/main/modelo.safetensors"
```

## Onde os ficheiros ficam

| Tipo | Pasta no Colab |
|------|----------------|
| Checkpoints | `/content/Fooocus/models/checkpoints/` |
| LoRAs | `/content/Fooocus/models/loras/` |
| VAE | `/content/Fooocus/models/vae/` |
| VAE approx | `/content/Fooocus/models/vae_approx/` |
| Prompt expansion | `/content/Fooocus/models/prompt_expansion/fooocus_expansion/` |

## Flags do notebook

| Variável | Default | Efeito |
|----------|---------|--------|
| `DOWNLOAD_ALL_PRESET_MODELS` | False | Ignorado: Colab lustify-only |
| `DOWNLOAD_NSFW_EXTRAS` | False | Ignorado: sem pacote multi-modelo |
| `FOOOCUS_PRESET` | lustify_v4 | Preset ao subir a UI |

## Presets no PC vs Colab

No workspace local (`presets/`) mantém-se pony, juggernaut, anteros, reed, etc. O Colab **não apaga** esses ficheiros no clone; apenas **não os baixa** na célula 2.

## Referência Civitai (identificação de versões)

- Lustify: https://civitai.com/models/573152

## Ficheiros deste workspace

- `fooocus_colab.ipynb` — notebook Colab (gerado)
- `COLAB-MODELS.md` — este guia
- `presets/lustify_v4.json` — preset Colab
- `scripts/build_colab_notebook.py`, `scripts/_colab_download_cell.py` — geradores

## Instrução após atualizar o repo

1. Abra o [notebook no Colab](https://colab.research.google.com/github/Claytonc40/generate-image/blob/main/fooocus_colab.ipynb).
2. **Re-execute** Config → Clone → Download → Iniciar.
3. Espere ~10–15 GB na célula Download antes de gerar imagens.

## Problemas comuns — célula Iniciar

### Notebook antigo (`entry_with_update.py`)

Se a célula **3) Iniciar Fooocus** ainda mostra `python entry_with_update.py` (sem `SKIP_GIT_UPDATE` / `launch.py`), o Colab abriu uma versão em cache ou anterior ao push. **Solução:** abra o link Colab abaixo (repo atualizado), ou cole a célula correta da secção seguinte e reexecute **Config → Clone → Download → Iniciar**.

### `entry_with_update.py` trava ou falha no Colab

Esse script chama `remote.fetch()` via **pygit2** antes de importar `launch`. No Colab isso costuma:

| Sintoma | Causa provável | O que fazer |
|---------|----------------|-------------|
| Célula “Iniciar” sem output por minutos | `git fetch` lento ou pendurado | Use `launch.py` com `SKIP_GIT_UPDATE = True` (notebook atual) |
| `Update failed` + mensagem pygit2 / SSL | Rede Colab ou validação Git | Idem — não precisa de fetch após `git clone` na célula 1 |
| `Failed to connect to github.com` | Firewall / instabilidade | Reexecute Clone; depois Iniciar com `launch.py` |
| `pygit2` ImportError | pip da célula 1 não rodou | Reexecute célula **1) Clone** (`pip install pygit2==1.15.1`) |

O clone raso (`--depth 1`) já traz o código necessário; **não** é obrigatório atualizar de novo no Colab antes de subir o Gradio.

### `ImportError: Failed to import CuPy` / `numpy.core.multiarray failed to import`

Ao subir o Fooocus, o `launch.py` importa `rembg` → `pymatting` → (opcional) `cupy`. No Colab com **Python 3.12**, o runtime costuma ter **NumPy 2.x** e **cupy-cuda12x** pré-instalados incompatíveis entre si. O CuPy quebra ao importar; o `pymatting` 1.1.15+ só ignora `ModuleNotFoundError`, não esse `ImportError`.

| Sintoma | Causa | O que fazer |
|---------|-------|-------------|
| Trace em `extras/inpaint_mask.py` → `rembg` → `pymatting` → `cupy` | NumPy/CuPy do Colab vs `requirements_versions.txt` | Reexecute a célula **1) Clone** do notebook atual (fix automático) |
| Mesmo erro após atualizar o repo | Notebook em cache / célula Clone antiga | Abra o [notebook no Colab](https://colab.research.google.com/github/Claytonc40/generate-image/blob/main/fooocus_colab.ipynb) e rode **Config → Clone → Download → Iniciar** |

A célula **1) Clone** do notebook gerado faz, após o `git clone`:

1. `pip uninstall` de `cupy` / `cupy-cuda*`
2. `numpy==1.26.4` (pin do `requirements_versions.txt`, compatível com torch 2.1)
3. `pip install -r requirements_versions.txt`
4. `pip uninstall` de cupy outra vez (evita reinstalação pelo ambiente Colab)
5. `rembg==2.0.57` + `pymatting==1.1.8` (versão sem import CuPy obrigatório no `foreground`)

**Fix manual** (se precisar colar numa célula extra antes de Iniciar):

```python
!pip uninstall -y cupy cupy-cuda12x cupy-cuda11x 2>/dev/null | true
!pip install -q --force-reinstall "numpy==1.26.4" "rembg==2.0.57" "pymatting==1.1.8"
```

Alternativa reportada na comunidade Fooocus: `numpy<2` + reinstalar `cupy-cuda12x` alinhado ao CUDA do runtime — só use se quiser GPU no pymatting; no Colab o inpaint/rembg em CPU é suficiente.

**Não** é necessário `Runtime → Restart` se você reexecutar Clone **antes** de Iniciar na mesma sessão (as deps ficam corretas para essa sessão).
