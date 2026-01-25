实现细节:
1. sh文件中训练时可以去掉eval_test，model_dir为对应的epoch0_step0
2. 推理时去掉do_train, 加上eval_test, 改为对应的best_epoch

arg对应的sh文件
1. 训练时去掉eval_test, gold_file为对应的eval的unified.jsonl
2. 推理时改为对应的test信息

需要注意的是cmnee和ace文件的区别
1. 对应的templates需要修改
2. arg文件中，max_seq_len为500
3. query_templates读取文件，编码方式改为gb18030

To run:
    CUDA_VISIBLE_DEVICES=0 bash code/script_args_qa_cmnee.sh