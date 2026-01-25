#!/bin/sh

export ACE_DIR=../dataset/cmnee_eeqa
export ACE_PRE_DIR=./trigger_qa_output_cmnee/epoch1-step0 # best trigger predictions

export ARG_QUERY_FILE=./question_templates/description_cmnee.csv
export DES_QUERY_FILE=./question_templates/description_cmnee.csv
export UNSEEN_ARG_FILE=./question_templates/unseen_args

echo "**************************"
echo "        template 3: des   "
echo "**************************"

echo "=========================================================================================="
echo "                                           real des_query + trigger verb                  "
echo "=========================================================================================="

## train script
# python code/run_args_qa.py \
#   --train_file $ACE_DIR/train.unified.jsonl \
#   --dev_file $ACE_PRE_DIR/eval_trigger_predictions.json \
#   --test_file $ACE_PRE_DIR/test_trigger_predictions.json \
#   --gold_file $ACE_DIR/test.unified.jsonl \
#   --train_batch_size 8 \
#   --eval_batch_size 8  \
#   --learning_rate 4e-5 \
#   --num_train_epochs 3 \
#   --output_dir args_qa_output_cmnee \
#   --nth_query 0 \
#   --normal_file $ARG_QUERY_FILE \
#   --des_file $DES_QUERY_FILE \
#   --eval_per_epoch 20 \
#   --max_seq_length 500 \
#   --n_best_size 20 \
#   --max_answer_length 15 \
#   --larger_than_cls \
#   --do_train \
#   --do_eval \
#   --model ../../../../MODELS/bert-base-chinese \
#   --model_dir args_qa_output_cmnee/epoch0-step0 \

## infer script
python code/run_args_qa.py \
  --train_file $ACE_DIR/train.unified.jsonl \
  --dev_file $ACE_PRE_DIR/eval_trigger_predictions.json \
  --test_file $ACE_PRE_DIR/test_trigger_predictions.json \
  --gold_file $ACE_DIR/test.unified.jsonl \
  --train_batch_size 8 \
  --eval_batch_size 8  \
  --learning_rate 4e-5 \
  --num_train_epochs 3 \
  --output_dir args_qa_output_cmnee \
  --nth_query 0 \
  --normal_file $ARG_QUERY_FILE \
  --des_file $DES_QUERY_FILE \
  --eval_per_epoch 20 \
  --max_seq_length 500 \
  --n_best_size 20 \
  --max_answer_length 15 \
  --larger_than_cls \
  --do_eval \
  --eval_test \
  --model ../../../../MODELS/bert-base-chinese \
  --model_dir args_qa_output_cmnee/epoch2-step0 \
#  To get final results on test, you need to (1) add eval_test; (2) set --model_dir to your model path for test (e.g., epoch-x-step-x)
