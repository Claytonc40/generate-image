# Fooocus no Google Colab — modelos e downloads

Guia em português para o notebook `fooocus_colab.ipynb`: o que é baixado automaticamente, URLs, presets e uso na interface.

## Ordem de execução no Colab

| Passo | Célula | O que faz |
|-------|--------|-----------|
| 1 | **Configuração** | Define `REPO_URL`, token Civitai, flags de download e preset inicial (`FOOOCUS_PRESET`) |
| 2 | **Clone** | `git clone` → `/content/Fooocus`, cria pastas `models/` |
| 3 | **Download** | Baixa checkpoints, loras e VAE (presets + extras NSFW) |
| 4 | **Iniciar** | `python entry_with_update.py --share --always-high-vram --preset …` |
| 5 | *(opcional)* | Download manual Civitai (colar URL da API) |

**Runtime:** GPU (T4 ou superior recomendado). **Disco:** conte o volume total abaixo (~40–70 GB se tudo estiver ativo).

## Avisos importantes

- **Conteúdo NSFW:** vários checkpoints são explícitos. Use apenas onde for legal e permitido.
- **Espaço em disco:** cada SDXL pesa ~6–7 GB. O pacote completo (presets Fooocus + 6 extras) pode passar de **50 GB**.
- **Sessão Colab:** arquivos em `/content` somem ao desligar a sessão — é preciso baixar de novo ou montar Google Drive.
- **Token Civitai:** crie em [civitai.com/user/account](https://civitai.com/user/account) → API Keys. Alguns modelos exigem login; no notebook use `CIVITAI_TOKEN = "seu_token"` ou variável de ambiente.
- **bigASP v2.5:** não é SDXL padrão (Flow Matching, só ComfyUI) — **não incluído** no download automático.
- **Fork:** para usar os presets deste workspace (`pony_v6`, `lustify_v4`, etc.), aponte `REPO_URL` para o seu repositório no GitHub ou faça upload do notebook após push.

## Como escolher o modelo na UI

1. Abra o link `gradio.live` gerado pelo Colab.
2. No topo, abra o menu **Preset** (ou passe `--preset nome` na célula de início).
3. Em **Model** / checkpoint, escolha o arquivo `.safetensors` correspondente.

| Preset | Checkpoint principal | Uso |
|--------|----------------------|-----|
| `default` | juggernautXL_v8Rundiffusion | Geral / equilíbrio |
| `realistic` | realisticStockPhoto_v20 | Fotos stock |
| `anime` | animaPencilXL_v500 | Anime |
| `pony_v6` | ponyDiffusionV6XL (+ VAE pony) | Anime/hentai estilo Pony |
| `lustify_v4` | lustifySDXLNSFW_v40Alpha | NSFW realista (Lustify v4) |
| `juggernaut_v9` | Juggernaut-XL_v9_RunDiffusionPhoto_v2 | Realismo + NSFW |
| `epicrealism_xl` | epicrealismXL_pureFix | Fotos realistas |
| `anteros_xxxl` | anterosXXXL_v10 | Photoreal NSFW forte |
| `reed_illustrious_v12` | reedXXXIllustrious_v120 | Ilustrado / semi-real NSFW |
| `sai` | sd_xl_base + refiner | SDXL oficial |
| `playground_v2.5` | playground-v2.5 | Estética Playground |

## Downloads automáticos — presets Fooocus (oficiais)

| Arquivo | URL |
|---------|-----|
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

## Downloads automáticos — 6 modelos SDXL solicitados

| Modelo | Arquivo no Colab | Fonte | URL direta |
|--------|------------------|-------|------------|
| **Lustify v4** | lustifySDXLNSFW_v40Alpha.safetensors | Civitai v4.0 alpha | https://civitai.com/api/download/models/926965 |
| **Lustify APEX v8** *(opcional)* | lustifySDXLNSFW_apexV8.safetensors | Civitai (mais recente) | https://civitai.com/api/download/models/2808677 |
| **Juggernaut XL v9** | Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors | HuggingFace | https://huggingface.co/RunDiffusion/Juggernaut-XL-v9/resolve/main/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors |
| **Epic Realism XL** | epicrealismXL_pureFix.safetensors | Civitai Pure_fix | https://civitai.com/api/download/models/2514955 |
| **Epic VX-FinalKiSS** *(opcional)* | epicrealismXL_vxFinalkiss.safetensors | Civitai | https://civitai.com/api/download/models/1063833 |
| **Anteros XXXL** | anterosXXXL_v10.safetensors | HF → fallback Civitai | https://huggingface.co/rosamelanopex/ModelsXL/resolve/e4d1f2bd7fd3078313bc5954ddc8de4760d38b5a/anterosXXXL_v10.safetensors |
| | | Civitai v1.0 fp16 | https://civitai.com/api/download/models/479579 |
| **Pony Diffusion V6 XL** | ponyDiffusionV6XL.safetensors + VAE | HuggingFace (preset pony_v6) | ver tabela acima |
| **REED_XXX Illustrious v12** | reedXXXIllustrious_v120.safetensors | Civitai | https://civitai.com/api/download/models/2852255 |
| **REED v14** *(opcional)* | reedXXXIllustrious_v140.safetensors | Civitai | https://civitai.com/api/download/models/2954011 |

### Lustify v4 no WebUI vs Colab

No A1111/WebUI o nome costuma ser `[SDXL] Lustify v4`. No Civitai a família **LUSTIFY!** inclui várias versões; o notebook usa **v4.0 alpha** (`926965`) por alinhar ao pedido “v4”. Para a build mais nova, ative `DOWNLOAD_LUSTIFY_APEX_V8 = True` (APEX V8, `2808677`).

Espelho HF (pode exigir aceitar conteúdo sensível na conta): [John6666/lustify-sdxl-nsfwsfw-v4-sdxl](https://huggingface.co/John6666/lustify-sdxl-nsfwsfw-v4-sdxl) — sem URL `resolve` estável listada aqui; prefira Civitai.

## Download manual (modelo sem URL estável)

1. Abra o modelo no Civitai → aba da versão → botão **Download** → copie o link da API (`/api/download/models/{id}`).
2. Na célula opcional do notebook:

```python
MANUAL_URL = "https://civitai.com/api/download/models/SEU_ID"
MANUAL_FILENAME = "nome_do_arquivo.safetensors"
```

3. Com token, se necessário: `?token=...` ou `CIVITAI_TOKEN` já configurado.

**Exemplo wget no terminal Colab:**

```bash
wget -c --content-disposition -O /content/Fooocus/models/checkpoints/modelo.safetensors \
  "https://civitai.com/api/download/models/ID?token=SEU_TOKEN"
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
| `DOWNLOAD_ALL_PRESET_MODELS` | True | Todos os URLs em `presets/*.json` |
| `DOWNLOAD_NSFW_EXTRAS` | True | Pacote dos 6 modelos + Pony |
| `DOWNLOAD_LUSTIFY_APEX_V8` | False | + Lustify APEX v8 |
| `DOWNLOAD_EPIC_VX_FINALKISS` | True | + epicrealismXL_vxFinalkiss |
| `DOWNLOAD_REED_V14` | False | + reed v14 em vez de só v12 |
| `FOOOCUS_PRESET` | default | Preset ao subir a UI |

## Páginas Civitai (referência)

- Lustify: https://civitai.com/models/573152
- Juggernaut XL: https://civitai.com/models/133005
- epiCRealism XL: https://civitai.com/models/277058
- Anteros XXXL: https://civitai.com/models/430454 (conteúdo maduro)
- Pony V6 XL: https://civitai.com/models/257749
- REED_XXX Illustrious: https://civitai.com/models/1717562

## Ficheiros alterados neste workspace

- `fooocus_colab.ipynb` — notebook Colab completo
- `COLAB-MODELS.md` — este guia
- `presets/lustify_v4.json`, `juggernaut_v9.json`, `epicrealism_xl.json`, `anteros_xxxl.json`, `reed_illustrious_v12.json`
- `scripts/build_colab_notebook.py`, `scripts/_colab_download_cell.py` — geradores do notebook
