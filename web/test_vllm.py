from vllm import LLM, SamplingParams

llm = LLM(
    model="facebook/opt-125m",   # change this with a higher capacity model if needed
    gpu_memory_utilization=0.5, 
    max_model_len=128
)

# Sampling parameters
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=64
)

# Test prompt
prompt = "Explain quantum computing in one sentence."

# Generate output
outputs = llm.generate([prompt], sampling_params)
for output in outputs:
    print(f"Prompt: {prompt}")
    print(f"Output: {output.outputs[0].text}")
