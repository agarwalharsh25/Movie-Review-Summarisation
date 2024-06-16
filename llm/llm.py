import cohere


class LLM:
    
    def __init__(self, api_key, llm='cohere'):
        self.llm = llm
        if llm == 'cohere':
            self.model = cohere.Client(api_key)
        else:
            raise ValueError(f'LLM {llm} not supported')

    def chat(self, prompt, preamble=None):
        response = None
        if self.llm == 'cohere' and self.model:
            if preamble:
                response = self.model.chat(message=prompt, preamble=preamble)
            else:
                response = self.model.chat(message=prompt)

            if response:
                response = response.text

        return response
