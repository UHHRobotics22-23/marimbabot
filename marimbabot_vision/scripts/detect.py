#!/usr/bin/env python3

import torch
from PIL import Image
from transformers import (DonutProcessor, VisionEncoderDecoderConfig,
                          VisionEncoderDecoderModel)

INPUT_FILE = './demo.png'
MODEL = './model'

# Load base model
ved_config = VisionEncoderDecoderConfig.from_pretrained(MODEL)
pre_processor = DonutProcessor.from_pretrained(MODEL)
model = VisionEncoderDecoderModel.from_pretrained(MODEL, ignore_mismatched_sizes=True, config=ved_config)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Load image
image = Image.open(INPUT_FILE).convert('RGB')

# Generate initial sequence
decoder_input_ids = pre_processor.tokenizer(
    "<s>",
    add_special_tokens=False,
    return_tensors="pt").input_ids

# Preprocess image
pixel_values = pre_processor(image, return_tensors="pt").pixel_values

# Run the model
outputs = model.generate(
    pixel_values.to(device),
    decoder_input_ids=decoder_input_ids.to(device),
    max_length=model.decoder.config.max_position_embeddings,
    early_stopping=True,
    pad_token_id=pre_processor.tokenizer.pad_token_id,
    eos_token_id=pre_processor.tokenizer.eos_token_id,
    use_cache=True,
    num_beams=1,
    bad_words_ids=[[pre_processor.tokenizer.unk_token_id]],
    return_dict_in_generate=True,
)

# Decode tokens
sequence = pre_processor.batch_decode(outputs.sequences, skip_special_tokens=True)[0]

print(sequence)

