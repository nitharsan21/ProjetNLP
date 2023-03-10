import tarfile
import os
import gpt_2_simple as gpt2

if __name__ == '__main__':

    model_name = "model_v5"
    if not os.path.isdir(os.path.join("models", model_name)):
        print("Downloading ", model_name, " model...")
        gpt2.download_gpt2(model_name=model_name)  # model is saved into current directory under /models/124M/

    # file_name = "writing_prompts.txt"

    # file_name = "../data/text_adventures.txt"
    # file_name = "C:/Users/nitha/PycharmProjects/ProjetNLP/data/text_adventures.txt"
    #
    # sess = gpt2.start_tf_sess()
    # gpt2.finetune(
    #     sess,
    #     file_name,
    #     multi_gpu=True,
    #     batch_size=8,
    #     learning_rate=0.0001,
    #     model_name=model_name,
    #     sample_every=1000,
    #     max_checkpoints=1,
    #     save_every=200,
    #     steps=600,
    # )
    #
    # gpt2.generate(sess)