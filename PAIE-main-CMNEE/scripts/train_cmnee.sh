if [ $# == 0 ] 
then
    SEED=42
    LR=2e-5
else
    SEED=$1
    LR=$2
fi

work_path=exps/cmnee/$SEED/$LR
mkdir -p $work_path

python engine.py \
    --model_type=paie \
    --dataset_type=cmnee \
    --model_name_or_path=../../../../MODELS/bart-base-chinese \
    --role_path=./data/dset_meta/description_cmnee.csv \
    --prompt_path=./data/prompts/prompts_cmnee_full.csv \
    --seed=$SEED \
    --output_dir=$work_path  \
    --learning_rate=$LR \
    --batch_size 4 \
    --eval_steps 500  \
    --max_steps=10000 \
    --max_enc_seq_length 500 \
    --max_prompt_seq_length 128 \
    --bipartite \