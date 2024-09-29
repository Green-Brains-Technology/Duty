import os
import subprocess
import tempfile
import asyncio
from reachllm import ReachLLM
from talk import Talk
from listen import Listen
import black
from black import format_str

class Midknight:
    def __init__(self, prompt):
        self.prompt = prompt
        self.talk = Talk()
        self.reach_llm = ReachLLM(api_key="YOUR_API_KEY")
        self.coderaw = self.reach_llm.input_output(prompt)
        clean_code = self.coderaw.replace("```python", "").replace("```", "")
        mode = black.FileMode(target_versions={black.TargetVersion.PY36})
        formatted_code = format_str(clean_code , mode=mode)  # Adjust mode as needed
        #print("Code:", formatted_code)
        output, error = self.run_code(formatted_code)
        
        if error:
            asyncio.run(self.talk.speak_text("Ermmmmmm frederick, there seem to be an error with code execution. I will need your attention."))
        else:
            asyncio.run(self.talk.speak_text("Finished successfully!"))
        
        print("Output:", output)
        print("Error:", error)
        
    def run_code(self, code):
        """
        This function takes a string of Python code, writes it to a temporary file,
        and executes the file using the subprocess module. It captures and returns
        the output and errors produced by the executed code.

        :param code: str: The AI-generated code to run.
        :return: tuple: A tuple containing the standard output and standard error.
        """
        try:
            # Create a temporary file to store the code
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
                temp_file_name = temp_file.name
                temp_file.write(code.encode('utf-8'))

            # Run the code using subprocess and capture the output and errors
            result = subprocess.run(
                ["python", temp_file_name],
                capture_output=True,
                text=True
            )

            # Read the output and errors
            stdout = result.stdout
            stderr = result.stderr

            return stdout, stderr

        finally:
            pass
            # Clean up the temporary file
            if os.path.exists(temp_file_name):
                os.remove(temp_file_name)
                
# Example usage
# if __name__ == "__main__":
#     ai_knight = Midknight(api_key="YOUR_API_KEY")

#     ai_generated_code = """
# print("Hello, world!")
# x = 10
# y = 20
# print(f"The sum of {{x}} and {{y}} is {{x + y}}")
# """
    


