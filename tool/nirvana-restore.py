import datetime
import json
import os
import shutil
import sys
from pathlib import Path

import lib

if __name__ == '__main__':
    lib.print_sep()
    print(f'>>> nirvana_restore [{datetime.datetime.now()}]')

    snapshot_dir = Path(os.environ['SNAPSHOT_PATH']).absolute().resolve()
    if not snapshot_dir.exists():
        print(f'Snapshot ({snapshot_dir}) does not exist.')
        lib.print_sep()
        sys.exit(0)

    print(
        f'Snapshot ({snapshot_dir}) contains the following files'
        ' (relative to the project directory):'
    )
    for dir_dirs_files in os.walk(snapshot_dir):
        for name in dir_dirs_files[2]:
            print(Path(dir_dirs_files[0] + '/' + name).relative_to(snapshot_dir))

    EXP_snapshot = snapshot_dir / lib.EXP_DIR.name
    if not EXP_snapshot.exists():
        print('Nothing to restore from the snapshot')
        lib.print_sep()
        sys.exit(0)

    json_output = snapshot_dir / 'json_output.json'
    if json_output.exists():
        shutil.copyfile(json_output, os.environ['JSON_OUTPUT_FILE'])

    for dirpath, _, filenames in os.walk(EXP_snapshot):
        dirpath = Path(dirpath)
        if (
            # Restore finished runs.
            'DONE' in filenames
            or (
                # Restore unfinished runs of `bin.tune.main`.
                'checkpoint.pt' in filenames
                and (
                    json.loads(dirpath.joinpath('report.json').read_text())['function']
                    == 'bin.tune.main'
                )
            )
        ):
            output = lib.EXP_DIR / dirpath.relative_to(EXP_snapshot)
            assert not output.exists()
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(dirpath, output)
            if 'DONE' in filenames:
                # Copy the snapshot directly to the output.
                lib.backup_output(output)
            print(f'Restored: {output}')
    snapshot_dir.joinpath('CHECKPOINTS_RESTORED')
    lib.print_sep()
