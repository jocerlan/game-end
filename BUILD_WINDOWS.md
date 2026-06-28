Resumo rápido — Gerar .exe para Windows

Opções recomendadas:

- Usar GitHub Actions (mais simples e reprodutível): faça push do repositório e execute o workflow `Build Windows EXE` (arquivo: .github/workflows/build-windows.yml). O artefato `ColetorMoedas-windows` conterá `dist/ColetorMoedas.exe`.

- Rodar localmente em Windows: abra PowerShell, crie/ative venv, e execute `scripts\build_windows.ps1`.

Notas:
- Não é confiável compilar um .exe do Windows diretamente no macOS com PyInstaller — usar runner Windows ou máquina Windows é o caminho seguro.
- O workflow já instala dependências, executa `img.py` para gerar `imagens/` e executa PyInstaller com `--add-data "imagens;imagens"` para embutir os assets.
