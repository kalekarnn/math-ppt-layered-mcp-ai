from typing import Dict, Any
from mcp import ClientSession

from logger_config import logger

class Perception:
    def __init__(self, session: ClientSession):
        self.session = session
        logger.info("Perception layer initialized")
    
    async def get_available_tools(self) -> Dict[str, Any]:
        """Perceive available tools from the environment"""
        logger.info("Getting available tools")
        tools_result = await self.session.list_tools()
        logger.debug(f"Retrieved {len(tools_result.tools)} tools")
        return tools_result.tools
    
    async def parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse and understand the response from LLM"""
        logger.info("Parsing response")
        response_type = None
        params = []
        
        try:
            # Remove any markdown code block formatting
            if response_text.startswith("```") and response_text.endswith("```"):
                response_text = response_text.strip("`").strip()
            
            if "FUNCTION_CALL:" in response_text:
                response_type = "function"
                function_part = response_text[response_text.index("FUNCTION_CALL:"):].split("\n")[0]
                _, params_str = function_part.split(":", 1)
                params = [p.strip() for p in params_str.split("|")]
            elif "POWERPOINT:" in response_text:
                response_type = "powerpoint"
                powerpoint_part = response_text[response_text.index("POWERPOINT:"):].split("\n")[0]
                _, params_str = powerpoint_part.split(":", 1)
                params = [p.strip() for p in params_str.split("|")]
            elif "FINAL_ANSWER:" in response_text:
                response_type = "final"
                _, answer = response_text.split(":", 1)
                params = [answer.strip()]
                
            logger.debug(f"Parsed response type: {response_type}, params: {params}")
            return {
                "type": response_type,
                "params": params
            }
        except Exception as e:
            print(f"Error parsing response: {e}")
            return {
                "type": "error",
                "params": [f"Failed to parse response: {str(e)}"]
            }