from typing import Dict, Any
from mcp import ClientSession
from logger_config import logger

class Action:
    def __init__(self, session: ClientSession):
        self.session = session
        logger.info("Action layer initialized")
    
    async def execute_function(self, func_name: str, params: list, tools: list) -> Any:
        """Execute a function call action"""
        tool = next((t for t in tools if t.name == func_name), None)
        if not tool:
            raise ValueError(f"Unknown tool: {func_name}")
            
        arguments = self._prepare_arguments(tool, params)

        logger.info(f"Executing function {tool.name} with arguments {arguments}")
        result = await self.session.call_tool(tool.name, arguments)
        return result
    
    def _prepare_arguments(self, tool: Any, params: list) -> Dict[str, Any]:
        """Prepare arguments according to tool schema"""
        schema = tool.inputSchema
        logger.info(f"Preparing arguments for {tool.name}")
        logger.info(f"Tool schema: {schema}")
        
        # Determine model name via $ref
        input_ref = schema.get("properties", {}).get("input", {}).get("$ref", "")
        model_name = input_ref.split("/")[-1] if input_ref.startswith("#/$defs/") else ""

        input_dict = {}
        if not params:
            if tool.name == 'open_powerpoint' or tool.name == 'close_powerpoint':
                return {}
            else:    
                raise ValueError(f"No parameters provided for {tool.name}")

        if model_name == 'StringInput':
            input_dict = {'string': str(params[0])}
        elif model_name == 'NumberInput':
            input_dict = {
                'a': int(params[0]) if len(params) > 0 else 0,
                'b': int(params[1]) if len(params) > 1 else 0
            }
        elif model_name == 'SingleNumberInput':
            input_dict = {'a': int(params[0])}
        elif model_name == 'ListInput':
            if isinstance(params[0], str):
                if params[0].startswith('[') and params[0].endswith(']'):
                    array_str = params[0].strip('[]')
                    numbers = [int(x.strip()) for x in array_str.split(',') if x.strip()]
                    input_dict = {'l': numbers}
                elif ',' in params[0]:
                    numbers = [int(x.strip()) for x in params[0].split(',')]
                    input_dict = {'l': numbers}
                else:
                    input_dict = {'l': [int(params[0])]}
            else:
                input_dict = {'l': [int(x) for x in params]}
        elif model_name == 'PowerPointTextInput':
            input_dict = {'text': str(params[0])}
        elif model_name == 'RectangleInput':
            input_dict = {
                'x1': int(params[0]) if len(params) > 0 else 1,
                'y1': int(params[1]) if len(params) > 1 else 1,
                'x2': int(params[2]) if len(params) > 2 else 2,
                'y2': int(params[3]) if len(params) > 3 else 2
            }
        elif model_name == 'ImageInput':
            input_dict = {'image_path': str(params[0])}
        elif model_name == 'FibonacciInput':
            input_dict = {'n': int(params[0])}
        else:
            # Generic case
            params_copy = list(params)
            properties = schema.get('properties', {})
            for param_name, param_info in properties.items():
                if not params_copy:
                    break
                value = params_copy.pop(0)
                param_type = param_info.get('type', 'string')
                input_dict[param_name] = self._convert_param_value(value, param_type)

        # 🔄 If using $ref, wrap inside "input"
        if model_name:
            return {'input': input_dict}
        else:
            return input_dict

    def _convert_param_value(self, value: str, param_type: str) -> Any:
        """Convert parameter value to correct type"""
        if param_type == 'integer':
            return int(value)
        elif param_type == 'number':
            return float(value)
        elif param_type == 'array':
            if value.startswith('[') and value.endswith(']'):
                array_str = value.strip('[]')
                return [int(x.strip()) for x in array_str.split(',')] if array_str else []
            elif ',' in value:
                return [int(x.strip()) for x in value.split(',')]
            return [int(value)]
        return value