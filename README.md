# Grades Horárias — UFBA/IGEO

Site estático para visualizar grades horárias por semestre.

## Estrutura

```
/
├── index.html          ← site principal
├── grade_generator.py  ← script para gerar grades
├── grades/
│   ├── grade_visual_2025-1.html
│   └── grade_visual_2025-2.html
└── README.md
```

## Como usar

### 1. Gerar uma grade nova

```bash
python grade_generator.py
```

O script vai perguntar o semestre e as matérias. Ao final, ele:
- Salva o HTML em `grades/grade_visual_SEMESTRE.html`
- Imprime o trecho que você precisa colar no `index.html`

### 2. Registrar no site

Abra `index.html` e encontre o array `SEMESTRES`. Adicione sua grade:

```js
const SEMESTRES = [
  { id: "2025-1", label: "2025.1", arquivo: "grades/grade_visual_2025-1.html" },
  { id: "2025-2", label: "2025.2", arquivo: "grades/grade_visual_2025-2.html" },
];
```

### 3. Publicar no GitHub Pages

```bash
git add .
git commit -m "Adiciona grade 2025.1"
git push
```

Ative o GitHub Pages em: **Settings → Pages → Deploy from branch → main / (root)**

Seu site vai ficar em: `https://SEU-USUARIO.github.io/NOME-DO-REPO/`
