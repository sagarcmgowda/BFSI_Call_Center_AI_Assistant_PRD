from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class SLMService:
    def __init__(self):
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            low_cpu_mem_usage=True
        )

        self.model.eval()

        # CPU optimization
        torch.set_num_threads(6)   # Adjust based on your CPU cores


    # ===============================
    # TIER 2 — Normal SLM Generation
    # ===============================
    def generate(self, query: str):

        messages = [
            {
                "role": "system",
                "content": "You are a professional BFSI call center assistant. "
                           "Provide a clear, compliant and concise answer. "
                           "Do not fabricate policies."
            },
            {
                "role": "user",
                "content": query
            }
        ]

        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(prompt, return_tensors="pt")

        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=60,
                do_sample=False,
                eos_token_id=self.tokenizer.eos_token_id
            )

        generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
        result = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)

        return result.strip()


    # =====================================
    # TIER 3 — STRICT RAG GROUNDED GENERATION
    # =====================================
    def generate_with_context(self, query: str, context: str):

        messages = [
            {
                "role": "system",
                "content": "You are a BFSI compliance assistant. "
                           "Answer ONLY using the provided policy context. "
                           "If the answer is not in the context, say: "
                           "'The requested information is not available in the policy context.'"
            },
            {
                "role": "user",
                "content": f"Policy Context:\n{context}\n\nQuestion:\n{query}"
            }
        ]

        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(prompt, return_tensors="pt")

        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=40,
                do_sample=False,
                eos_token_id=self.tokenizer.eos_token_id
            )

        generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
        result = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)

        return result.strip()
