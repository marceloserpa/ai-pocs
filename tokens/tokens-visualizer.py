from transformers import AutoTokenizer

text = """
English and CAPITALIZATION
🎵鸟
show_tokens False None elif == >= else: two tabs:" " Three tabs: "
"
12.0*50=600
"""



colors_list = [
    '102;194;165', '252;141;98', '141;160;203',
    '231;138;195', '166;216;84', '255;217;47'
]
def show_tokens(sentence, tokenizer_name):
    print("\n## tokenizer name: " + tokenizer_name + " ##")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    token_ids = tokenizer(sentence).input_ids
    for idx, t in enumerate(token_ids):
        print(
            f'\x1b[0;30;48;2;{colors_list[idx % len(colors_list)]}m' +
            tokenizer.decode(t) +
            '\x1b[0m',
            end=' '
        )


show_tokens(text, "bert-base-uncased")
show_tokens(text, "bert-base-cased")
show_tokens(text, "gpt2")
show_tokens(text, "google/flan-t5-xxl")
show_tokens(text, "bigcode/starcoder2-15b")
show_tokens(text, "facebook/galactica-1.3b")
show_tokens(text, "microsoft/Phi-3-mini-4k-instruct")