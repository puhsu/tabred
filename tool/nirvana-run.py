# >>> nirvana-run.py <<<
# Run jobs on nirvana

import os
from pathlib import Path

import nirvana_api
import vh
import urllib3

import lib

# Some Internal TLS stuff
os.environ['REQUESTS_CA_BUNDLE'] = '/usr/local/share/ca-certificates/YandexInternalRootCA.crt'
urllib3.disable_warnings()

NIRVANA_TOKEN = (Path.home()/'.nirvana/token').read_text().strip()
NIRVANA_YT_SECRET = 'irubachev-yt-2023-08-14'
NIRVANA_SSH_SECRET = 'github-d'
NIRVANA = nirvana_api.NirvanaApi(NIRVANA_TOKEN, ssl_verify=False)
WORKFLOW_ID = "1f79a662-4caf-42db-9554-06920978e3a7"

REPOSITORY_URL = 'git@github.com:puhsu/tabular-dl-tabred.git'
REPOSITORY_BRANCH = 'main'
REPOSITORY_NAME = REPOSITORY_URL.rsplit('/', 1)[1].replace('.git', '')

# All the latest datasets
DATASETS_URL = 'https://proxy.sandbox.yandex-team.ru/6427855148'


def run_graph(
    *,
    commands: list[str],
    comment: str,
    priority: str,
    n_gpus: int,
    n_cpu_cores: int,
    disk_gb: int,
    memory_gb: int,
    gpu_memory_gb: int,
    ttl_hours: int,
    debug_timeout: int = 0,
    debug: bool = False
):
    assert commands
    assert comment
    assert priority in ['low', 'normal', 'high']
    assert n_gpus >= 0
    assert 1 <= n_cpu_cores < 255
    for cmd in commands:
        if 'tune.py' in cmd or 'go.py' in cmd or 'tune2.py' in cmd or 'go2.py' in cmd:
            assert ' --continue' in cmd

    print(f'>>> {comment}')
    if debug:
        print(f'[P] {priority} [MEM] {memory_gb} [DISK] {disk_gb} [TTL] {ttl_hours}')
        print('\n'.join(commands))
        print()
        return
    sep = '=' * 30
    all_commands = [
        'export MAMBA_ROOT_PREFIX="/micromamba"',
        'export PYTHON_MAIN_ENV=$MAMBA_ROOT_PREFIX/envs/main',
        'export PATH=$PATH:$PYTHON_MAIN_ENV/bin',
        'export PYTHON_CMD=$PYTHON_MAIN_ENV/bin/python',
        'export PROJECT_DIR=${SOURCE_CODE_PATH}/' + REPOSITORY_NAME,
        'export CUDA_VISIBLE_DEVICES="{}"'.format(",".join(map(str, range(n_gpus)))),
        'export YT_PROXY=hahn.yt.yandex.net',
        f'',
        
        '$PYTHON_CMD -mpip install -e $PROJECT_DIR',

        f'echo {sep}',
        'mv $INPUT_PATH/data-tabred $PROJECT_DIR/data',
        'cd $PROJECT_DIR',
        'pwd',
        'ls',
        'printenv',
        f'',

        f'echo {sep}',
        '$PYTHON_CMD tool/nirvana-restore.py',
        f'',
        
        f'echo {sep}',
    ] + [x.replace("python", "$PYTHON_CMD") for x in commands]
    del commands, sep

    with vh.Graph() as graph:
        clone_repo_op = vh.op(id='a918d982-9a42-4519-884b-f8759e41dc08')  # clone-a-repo-ext
        curl_op = vh.op(id='86dcacf7-ff24-44f1-955f-1781f65781c0')
        python_deep_learning_op = vh.op(id='78b7c7c8-2a31-4cd6-b9e0-bb103157a305')  # python3-dl 6.3.35

        python_deep_learning_op(
            _inputs=dict(
                script=clone_repo_op(
                    repo=REPOSITORY_URL,
                    folder_name=REPOSITORY_NAME,
                    commit_or_branch=REPOSITORY_BRANCH,
                    key=NIRVANA_SSH_SECRET,
                ),
                data=[curl_op(url=DATASETS_URL)],
            ),
            base_layer='NONE',
            run_command='\n'.join(all_commands),
            additional_layers=['bdad7b9d-b619-4d2b-b11b-bd3961091d68'],  # my tabred layer
            gpu_count=n_gpus,
            gpu_type='CUDA_8_0',
            strict_gpu_type=True,
            gpu_max_ram=gpu_memory_gb * 1024,
            max_disk=disk_gb * 1024,
            max_ram=memory_gb * 1024,
            cpu_cores_usage=n_cpu_cores * 100,
            ttl=ttl_hours * 60,
            debug_timeout=debug_timeout, # minutes
            yt_token=NIRVANA_YT_SECRET,
        )

    keeper = vh.run(
        graph=graph,
        oauth_token=NIRVANA_TOKEN,
        quota='yr-other',
        workflow_guid=WORKFLOW_ID,
        description=comment,
        start=False,
    )
    info = keeper.get_workflow_info()
    NIRVANA.edit_workflow(
        workflow_id=info.workflow_id,
        workflow_instance_id=info.workflow_instance_id,
        execution_params={'workflowPriority': priority},
    )
    NIRVANA.start_workflow(
        workflow_id=info.workflow_id, workflow_instance_id=info.workflow_instance_id
    )




count = 0

for m in [
    # 'tabr',
    # 'tabr-causal',
    # 'ft_transformer',
    # "mlp",
    # "mlp-plr",
    # "xgboost_",
    # "resnet",
    # "snn",
    # "dcn2",
    # "catboost_",
    # "lightgbm_",
    "trompt",
    # "coral",
]:
    for d in [
        "sberbank-housing",
        "ecom-offers",
        # "homecredit-default",
        # 'maps-routing',
        'cooking-time',
        'delivery-eta',
        'weather',
        'homesite-insurance',
    ]:
        if m == 'trompt':
            if d not in ["ecom-offers", "homesite-insurance"]:
                function = 'bin.trompt.main'
            else:
                function = 'bin.trompt_binclass.main'

            c = f'python bin/evaluate.py exp/{m}/{d}/default-evaluation --function {function}'
        elif m == 'catboost_':
            c = f'python bin/tune.py exp/{m}/{d}/tuning.toml --continue'
        else:
            c = f'python bin/go.py exp/{m}/{d}/tuning.toml --continue'

        run_graph(
            commands = [
                c,
            ],
            comment=c.split()[2],
            priority='high',
            n_gpus=1,
            n_cpu_cores=4,
            disk_gb=100, 
            memory_gb=200, gpu_memory_gb=60, ttl_hours=120,
            debug_timeout=30,
            debug=False
        )


