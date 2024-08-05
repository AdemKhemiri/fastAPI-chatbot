from langchain.tools import BaseTool
class Calculator(BaseTool):
    name = "calculator"
    description = "Use this tool for math operations. It requires numexpr syntax. Use it always you need to solve any math operation. Be sure syntax is correct."

    def _run(self, expression: str):
      try:
        return ne.evaluate(expression).item()
      except Exception:
        return "This is not a numexpr valid syntax. Try a different syntax."

    def _arun(self, radius: int):
        raise NotImplementedError("This tool does not support async")

calculator_tool = Calculator()