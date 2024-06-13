# TabReD: A Benchmark of Tabular Machine Learning in-the-Wild

Suplementary code for the submission.

> Despite the recent advances in tabular machine learning (ML) research reported on existing academic benchmarks, the question of methods transferability to the real-world ML applications remains underexplored. One major obstacle is the lack of representative tabular ML application datasets, which are often proprietary and unavailable to the academic community. To facilitate transferability of tabular ML research and bridge the gap between academic benchmarks and real-world ML applications, we introduce the TabReD benchmark -- a collection of eight industrial-grade tabular datasets covering a wide range of domains from finance to food delivery services. All datasets in the TabReD benchmark possess a gradual temporal shift between the train/test subsets, closer resembling common model deployment scenarios. Furthermore, we make sure that all datasets in the benchmark are inherently tabular and do not contain data leakage issues -- which is not always the case for the existing benchmarks. We assess the performance of state-of-the-art tabular models on the new benchmark and observe that general progress in the field of tabular DL transfers to the more realistic settings introduced with TabReD, with exceptions in recent retrieval and attention-based tabular models, that prove to be less beneficial than simpler MLP-based solutions. We also show that accounting for temporal shift in evaluation leads to differences in ranking and relative performance of methods, compared to evaluation on random data splits.


## Repository Structure

- [`./preprocessing`](./preprocessing) directory contains preprocessing scripts for all the datasets
- [`./exp`](./exp) all exeperiment logs are in this folder
- [`./bin`](./bin) scripts for launching the experiments
- [`./lib`](./lib) library, dataloading, utilities 

## Environment

There are two environments: one for local development on machines without gpus -
`tabred-env-local.yaml`, another for the machines with GPUs `tabred-env.yaml`.

To create the environment with all the dependencies run `micromamba create -f` with the env file of
choice (for example `micromamba create -f tabred-env.yaml` on a server with GPUs).

## Example

To reproduce results for the MLP on the maps-routing dataset.

1. Create an environment
2. Create dataset (run preprocessing script)
3. Run `export CUDA_VISIBLE_DEVICES=0` (or whatever device you like)
4. Run `python bin/go.py exp/mlp/maps-routing/tuning.toml --force` (force, deletes the existing outputs)

## Dataset Details

There is also a [datasheet](./datasheet.md) for the benchmark.
