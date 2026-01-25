#! /bin/bash

NUM_GPUS=$1
shift

python -m torch.distributed.launch --nproc_per_node ${NUM_GPUS} --master_port 29503 run_dee_task.py $*
