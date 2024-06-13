export CUDA_VISIBLE_DEVICES=0

python bin/xgboost_.py exp/temporal-shift-analysis/xgboost_/homesite-insurance-random-0/evaluation/0.toml --force
python bin/xgboost_.py exp/temporal-shift-analysis/xgboost_/ecom-offers-random-0/evaluation/0.toml --force
python bin/xgboost_.py exp/temporal-shift-analysis/xgboost_/ecom-offers-random-2/evaluation/1.toml --force
python bin/xgboost_.py exp/temporal-shift-analysis/xgboost_/ecom-offers-sliding-window-2/evaluation/0.toml --force
python bin/xgboost_.py exp/temporal-shift-analysis/xgboost_/homecredit-default-random-0/evaluation/0.toml --force
python bin/xgboost_.py exp/temporal-shift-analysis/xgboost_/homecredit-default-sliding-window-0/evaluation/0.toml --force
python bin/xgboost_.py exp/temporal-shift-analysis/xgboost_/homecredit-default-sliding-window-1/evaluation/0.toml --force
python bin/xgboost_.py exp/temporal-shift-analysis/xgboost_/sberbank-housing-random-2/evaluation/0.toml --force
python bin/xgboost_.py exp/temporal-shift-analysis/xgboost_/sberbank-housing-sliding-window-0/evaluation/0.toml --force
python bin/xgboost_.py exp/temporal-shift-analysis/xgboost_/sberbank-housing-sliding-window-0/evaluation/1.toml --force
python bin/xgboost_.py exp/temporal-shift-analysis/xgboost_/sberbank-housing-sliding-window-1/evaluation/1.toml --force
python bin/xgboost_.py exp/temporal-shift-analysis/xgboost_/delivery-eta-random-0/evaluation/1.toml --force
python bin/xgboost_.py exp/temporal-shift-analysis/xgboost_/weather-random-0/evaluation/0.toml --force
python bin/xgboost_.py exp/temporal-shift-analysis/xgboost_/weather-sliding-window-0/evaluation/12.toml --force


# CUDA_VISIBLE_DEVICES=0 python bin/ffn.py exp/mlp-plr/homesite-insurance-sliding-window-1/test-run.toml --force
# CUDA_VISIBLE_DEVICES=0 python bin/ffn.py exp/mlp-plr/homesite-insurance-random-1/test-run.toml --force
# CUDA_VISIBLE_DEVICES=0 python bin/ffn.py exp/mlp-plr/homesite-insurance-sliding-window-2/test-run.toml --force
# CUDA_VISIBLE_DEVICES=0 python bin/ffn.py exp/mlp-plr/homesite-insurance-random-2/test-run.toml --force


# CUDA_VISIBLE_DEVICES=0 python bin/xgboost_.py exp/xgboost_/homesite-insurance-sliding-window-1/test-run.toml
# CUDA_VISIBLE_DEVICES=0 python bin/xgboost_.py exp/xgboost_/homesite-insurance-random-1/test-run.toml
# CUDA_VISIBLE_DEVICES=0 python bin/xgboost_.py exp/xgboost_/homesite-insurance-sliding-window-2/test-run.toml
# CUDA_VISIBLE_DEVICES=0 python bin/xgboost_.py exp/xgboost_/homesite-insurance-random-2/test-run.toml

# export CUDA_VISIBLE_DEVICES=0

# python bin/tabr.py exp/tabr/homesite-insurance-random-1/test-run.toml 
# python bin/tabr.py exp/tabr/homesite-insurance-random-2/test-run.toml 
# python bin/tabr.py exp/tabr/homesite-insurance-sliding-window-0/test-run.toml 
# python bin/tabr.py exp/tabr/homesite-insurance-sliding-window-1/test-run.toml 
# python bin/tabr.py exp/tabr/homesite-insurance-sliding-window-2/test-run.toml 
