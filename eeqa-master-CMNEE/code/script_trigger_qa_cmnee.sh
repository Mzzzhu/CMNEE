#!/bin/sh

export data_DIR=../dataset/cmnee_eeqa


echo "=========================================================================================="
echo "                                          query 5                                         "
echo "=========================================================================================="

python code/run_trigger_qa.py \
  --train_file $data_DIR/train.unified.jsonl \
  --dev_file $data_DIR/valid.unified.jsonl  \
  --test_file $data_DIR/test.unified.jsonl \
  --train_batch_size 8 \
  --eval_batch_size 8  \
  --eval_per_epoch 20 \
  --num_train_epochs 3 \
  --output_dir trigger_qa_output_cmnee \
  --learning_rate 4e-5 \
  --nth_query 5 \
  --warmup_proportion 0.1 \
  --model ../../../../MODELS/bert-base-chinese \
  --do_eval \
  --eval_test \
  --model_dir trigger_qa_output_cmnee_0921/epoch1-step0 \

  # To get final results on test, you need to (1) add eval_test; (2) set --model_dir to your model path for test (e.g., epoch-x-step-x)