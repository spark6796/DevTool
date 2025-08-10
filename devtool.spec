# -*- mode: python ; coding: utf-8 -*-
import os

# Collect template files
template_files = []
template_dir = 'src/devtool/templates'
for root, dirs, files in os.walk(template_dir):
    for file in files:
        src_path = os.path.join(root, file)
        # Convert source path to destination path in the bundle
        rel_path = os.path.relpath(src_path, template_dir)
        dest_path = os.path.join('devtool', 'templates', rel_path)
        template_files.append((src_path, os.path.dirname(dest_path)))

# Collect CSS files
css_files = [
    ('src/devtool/app.tcss', 'devtool')
]

# Collect all data files
datas = template_files + css_files

a = Analysis(
    ['src/devtool/__main__.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'devtool.app',
        'devtool.config',
        'devtool.screens.new_project',
        'devtool.screens.react_config',
        'devtool.screens.svelte_config',
        'devtool.screens.fastapi_config',
        'devtool.screens.stats',
        'devtool.project_creators.react_creator',
        'devtool.project_creators.svelte_creator',
        'devtool.project_creators.fastapi_creater',
        'devtool.utils.project_validator',
        'devtool.widgets.home',
        'textual',
        'textual.app',
        'textual.screen',
        'textual.widget',
        'textual.widgets',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='devtool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
