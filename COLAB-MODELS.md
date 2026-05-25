# Fooocus no Google Colab — modelos e downloads

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Claytonc40/generate-image/blob/main/fooocus_colab.ipynb)

Guia em português para o notebook `fooocus_colab.ipynb` no repositório [Claytonc40/generate-image](https://github.com/Claytonc40/generate-image): o que é baixado automaticamente, URLs **apenas HuggingFace** (ou mirrors públicos), presets e uso na interface.

## Ordem de execução no Colab

| Passo | Célula | O que faz |
|-------|--------|-----------|
| 1 | **Configuração** | Define `REPO_URL`, flags de download e preset inicial (`FOOOCUS_PRESET`) |
| 2 | **Clone** | `git clone` → `/content/Fooocus`, cria pastas `models/` |
| 3 | **Download** | Baixa checkpoints, loras e VAE (presets + extras NSFW) via HuggingFace |
| 4 | **Iniciar** | `python entry_with_update.py --share --always-high-vram --preset …` |
| 5 | *(opcional)* | Download manual com URL `resolve/main` (ex.: REED, Lustify APEX) |

**Runtime:** GPU (T4 ou superior recomendado). **Disco:** conte o volume total abaixo (~35–60 GB se tudo estiver ativo).

## Avisos importantes

- **Conteúdo NSFW:** vários checkpoints são explícitos. Use apenas onde for legal e permitido.
- **Espaço em disco:** cada SDXL pesa ~6–7 GB. O pacote NSFW automático não inclui REED nem Lustify APEX (sem espelho HF de ficheiro único).
- **Sessão Colab:** arquivos em `/content` somem ao desligar a sessão — é preciso baixar de novo ou montar Google Drive.
- **Sem Civitai:** o fluxo principal **não** usa token nem URLs `civitai.com`. Downloads inválidos (&lt;100 MB) falham com mensagem clara em vez de “ok 0 GB”.
- **Repositório:** o notebook clona por padrão `https://github.com/Claytonc40/generate-image.git` (branch `main`), com presets deste workspace (`pony_v6`, `lustify_v4`, etc.).

## Como escolher o modelo na UI

1. Abra o link `gradio.live` gerado pelo Colab.
2. No topo, abra o menu **Preset** (ou passe `--preset nome` na célula de início).
3. Em **Model** / checkpoint, escolha o arquivo `.safetensors` correspondente.

| Preset | Checkpoint principal | Download automático |
|--------|----------------------|---------------------|
| `default` | juggernautXL_v8Rundiffusion | Sim (HF) |
| `realistic` | realisticStockPhoto_v20 | Sim (HF) |
| `anime` | animaPencilXL_v500 | Sim (HF) |
| `pony_v6` | ponyDiffusionV6XL (+ VAE pony) | Sim (HF) |
| `lustify_v4` | lustifySDXLNSFW_v40Alpha | Sim (HF, espelho v40) |
| `juggernaut_v9` | Juggernaut-XL_v9_RunDiffusionPhoto_v2 | Sim (HF) |
| `epicrealism_xl` | epicrealismXL_pureFix | Sim (HF) |
| `anteros_xxxl` | anterosXXXL_v10 | Sim (HF) |
| `reed_illustrious_v12` | reedXXXIllustrious_v120 | **Manual** (sem HF) |
| `sai` | sd_xl_base + refiner | Sim (HF) |
| `playground_v2.5` | playground-v2.5 | Sim (HF) |

## Downloads automáticos — presets Fooocus (oficiais)

| Arquivo | URL HuggingFace |
|---------|-----------------|
| juggernautXL_v8Rundiffusion.safetensors | https://huggingface.co/lllyasviel/fav_models/resolve/main/fav/juggernautXL_v8Rundiffusion.safetensors |
| realisticStockPhoto_v20.safetensors | https://huggingface.co/lllyasviel/fav_models/resolve/main/fav/realisticStockPhoto_v20.safetensors |
| animaPencilXL_v500.safetensors | https://huggingface.co/mashb1t/fav_models/resolve/main/fav/animaPencilXL_v500.safetensors |
| playground-v2.5-1024px-aesthetic.fp16.safetensors | https://huggingface.co/mashb1t/fav_models/resolve/main/fav/playground-v2.5-1024px-aesthetic.fp16.safetensors |
| sd_xl_base_1.0_0.9vae.safetensors | https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0_0.9vae.safetensors |
| sd_xl_refiner_1.0_0.9vae.safetensors | https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0_0.9vae.safetensors |
| ponyDiffusionV6XL.safetensors | https://huggingface.co/mashb1t/fav_models/resolve/main/fav/ponyDiffusionV6XL.safetensors |
| ponyDiffusionV6XL_vae.safetensors *(pasta vae)* | https://huggingface.co/mashb1t/fav_models/resolve/main/fav/ponyDiffusionV6XL_vae.safetensors |
| sd_xl_offset_example-lora_1.0.safetensors *(lora)* | https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_offset_example-lora_1.0.safetensors |
| SDXL_FILM_PHOTOGRAPHY_STYLE_V1.safetensors *(lora)* | https://huggingface.co/mashb1t/fav_models/resolve/main/fav/SDXL_FILM_PHOTOGRAPHY_STYLE_V1.safetensors |

## Downloads automáticos — pacote NSFW/realista (6 modelos)

| Modelo | Arquivo no Colab | URL HuggingFace |
|--------|------------------|-----------------|
| **Lustify v4** | lustifySDXLNSFW_v40Alpha.safetensors | https://huggingface.co/xxxpo13/LUSTIFY_SDXL/resolve/main/lustifySDXLNSFWSFW_v40.safetensors |
| **Juggernaut XL v9** | Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors | https://huggingface.co/RunDiffusion/Juggernaut-XL-v9/resolve/main/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors |
| **Epic Realism XL Pure Fix** | epicrealismXL_pureFix.safetensors | https://huggingface.co/123543o/124052/resolve/main/checkpoints/XL/epicrealismXL_pureFix.safetensors |
| **Epic VX-FinalKiSS** *(opcional)* | epicrealismXL_vxFinalkiss.safetensors | https://huggingface.co/John6666/epicrealism-xl-v8kiss-sdxl/resolve/main/epicrealismXL_vx1Finalkiss.safetensors |
| **Anteros XXXL** | anterosXXXL_v10.safetensors | https://huggingface.co/rosamelanopex/ModelsXL/resolve/e4d1f2bd7fd3078313bc5954ddc8de4760d38b5a/anterosXXXL_v10.safetensors |
| **Pony Diffusion V6 XL** | ponyDiffusionV6XL.safetensors + VAE | ver tabela acima |

### Notas sobre espelhos HF

- **Lustify v4:** o ficheiro no HF chama-se `lustifySDXLNSFWSFW_v40.safetensors` (repo `xxxpo13/LUSTIFY_SDXL`); no Colab é guardado como `lustifySDXLNSFW_v40Alpha.safetensors` para o preset `lustify_v4`.
- **Epic vxFinalkiss:** espelho `epicrealismXL_vx1Finalkiss` (variante próxima no mesmo repositório John6666).
- Repositórios NSFW no HF podem pedir confirmação de idade na conta.

## Sem download automático (upload manual)

| Modelo | Arquivo | Motivo |
|--------|---------|--------|
| **REED Illustrious v12** | reedXXXIllustrious_v120.safetensors | Sem checkpoint `.safetensors` único no HF (só Civitai / diffusers fragmentado) |
| **REED v14** *(opcional)* | reedXXXIllustrious_v140.safetensors | Idem |
| **Lustify APEX v8** *(opcional)* | lustifySDXLNSFW_apexV8.safetensors | Sem espelho HF de checkpoint completo (só variantes quantizadas para NPU) |

Coloque o ficheiro em `/content/Fooocus/models/checkpoints/` ou use a célula opcional com uma URL `resolve/main` se encontrar um espelho.

## Download manual (célula opcional)

```python
MANUAL_URL = "https://huggingface.co/SEU_REPO/resolve/main/modelo.safetensors"
MANUAL_FILENAME = "nome_do_arquivo.safetensors"
```

**Exemplo wget no terminal Colab:**

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

O Fooocus também baixa na primeira execução (expansion, inpaint, controlnet, etc.) via `entry_with_update.py` — isso é independente desta célula de checkpoints.

## Flags do notebook

| Variável | Default | Efeito |
|----------|---------|--------|
| `DOWNLOAD_ALL_PRESET_MODELS` | True | Todos os URLs HF em `presets/*.json` |
| `DOWNLOAD_NSFW_EXTRAS` | True | Pacote dos 6 modelos + Pony (sem REED) |
| `DOWNLOAD_LUSTIFY_APEX_V8` | False | Aviso: sem HF; upload manual |
| `DOWNLOAD_EPIC_VX_FINALKISS` | True | + epic vxFinalkiss (espelho vx1Finalkiss) |
| `DOWNLOAD_REED_V14` | False | Aviso: sem HF; upload manual |
| `FOOOCUS_PRESET` | default | Preset ao subir a UI |

## Referência Civitai (só para identificar versões)

- Lustify: https://civitai.com/models/573152
- Juggernaut XL: https://civitai.com/models/133005
- epiCRealism XL: https://civitai.com/models/277058
- Anteros XXXL: https://civitai.com/models/430454
- Pony V6 XL: https://civitai.com/models/257749
- REED_XXX Illustrious: https://civitai.com/models/1717562

## Ficheiros deste workspace

- `fooocus_colab.ipynb` — notebook Colab
- `COLAB-MODELS.md` — este guia
- `presets/lustify_v4.json`, `juggernaut_v9.json`, `epicrealism_xl.json`, `anteros_xxxl.json`, `reed_illustrious_v12.json`, `pony_v6.json`
- `scripts/build_colab_notebook.py`, `scripts/_colab_download_cell.py` — geradores do notebook

## Instrução após atualizar o repo

1. Abra o [notebook no Colab](https://colab.research.google.com/github/Claytonc40/generate-image/blob/main/fooocus_colab.ipynb) (ou faça push de `fooocus_colab.ipynb` para `Claytonc40/generate-image`).
2. **Re-execute a célula 2) Download** (e a de clone se o repo mudou).
3. Se usar preset `reed_illustrious_v12`, faça upload manual do checkpoint antes de gerar imagens.
