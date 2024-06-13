# >>> nirvana-download.py <<<
# Run jobs on nirvana

import os
from pathlib import Path

import nirvana_api
import urllib3
from tqdm.auto import tqdm

import lib

# Some Internal TLS stuff
os.environ['REQUESTS_CA_BUNDLE'] = '/usr/local/share/ca-certificates/YandexInternalRootCA.crt'
urllib3.disable_warnings()


NIRVANA_TOKEN = (Path.home()/'.nirvana/token').read_text().strip()
NIRVANA_YT_SECRET = 'irubachev-yt-2023-08-14'
NIRVANA_SSH_SECRET = 'github-d'
NIRVANA = nirvana_api.NirvanaApi(NIRVANA_TOKEN, ssl_verify=False)
WORKFLOW_ID = "1f79a662-4caf-42db-9554-06920978e3a7"

PERSONAL_DIR = lib.PROJECT_DIR / 'dev-irubachev'
DOWNLOAD_DIR = PERSONAL_DIR / 'nirvana_results'
DOWNLOAD_DIR.mkdir(exist_ok=True, parents=True)
LOG_PATH = PERSONAL_DIR / 'nirvana_log.json'

if not LOG_PATH.exists():
    print("creating new log file")
    lib.dump_json({}, LOG_PATH)

LOG = lib.load_json(LOG_PATH)


def nirvana_get_workflow_instance_results(workflow_instance_id):
    results = NIRVANA.get_block_results(
        block_patterns={'code': '_vh__78b7c7c8-2a31-4cd6-b9e0-bb103157a305'},
        workflow_instance_id=workflow_instance_id
    )
    if not results:
        return None
    return {x['endpoint']: x['directStoragePath'] for x in results[0]['results']}


def fetch_info(workflow_id, instance_id, completed=True):
    full_id = f'{workflow_id}/{instance_id}'
    if full_id in LOG:
        return None

    info = vars(NIRVANA.get_workflow_meta_data(workflow_instance_id=instance_id))
    if info['archived']:
        return None
    if ('completed' not in info) ^ (not completed):
        return None
    if 'instanceComment' not in info:
        print('[NO COMMENT]', full_id)
        return None

    info['_full_id'] = full_id
    comment = info.get('instanceComment', '[NO COMMENT]')
    for c in [' ', '(', ')', '/', '|', ',', '[', ']', "'"]:
        comment = comment.replace(c, '_')
    info['_fullname'] = f'{comment}___{instance_id}'
    info['_result'] = nirvana_get_workflow_instance_results(instance_id)
    return info


instance_ids = [x['instanceId'] for x in NIRVANA.find_workflows(WORKFLOW_ID)]
instances = [fetch_info(WORKFLOW_ID, x, completed=True) for x in tqdm(instance_ids)]
instances = [x for x in instances if x is not None]
instances.sort(key=lambda x: x['_fullname'])
for x in instances:
    print(x["_fullname"])


import subprocess
import tarfile

for instance in instances:
    assert instance is not None
    fullname = instance["_fullname"]
    full_id = instance["_full_id"]

    # if full_id in LOG:
    #     print(f"Already done with: {fullname}")
    #     continue

    print(fullname)
    path = DOWNLOAD_DIR / f'{instance["_fullname"][:100]}.tar'
    path.parent.mkdir(exist_ok=True, parents=True)
    if not path.exists():
        try:
            subprocess.run(
                ['wget', instance['_result']['data'], '-O', str(path)],
                stderr=subprocess.DEVNULL,
                check=True,
            )
        except Exception as e:
            print('FAIL', e)
            path.unlink(True)
            continue

    with tarfile.open(path) as archive:
        files = [
            x[2:] if x.startswith('./') else x
            for x in archive.getnames()
            if x not in ['.', './'] and '.' in x.split('/')[-1]
        ]
        archive.extractall(lib.PROJECT_DIR)

    os.remove(path)

    LOG[full_id] = instance
    LOG[full_id]['_files'] = files
    lib.dump_json(LOG, LOG_PATH)
