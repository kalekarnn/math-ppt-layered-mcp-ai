from typing import Dict, Any
import asyncio
from google import genai
from agent.prompts import create_system_prompt

from logger_config import logger

class Decision:
    def __init__(self, client: genai.Client):
        self.client = client
        logger.info("Decision layer initialized")
    
    async def generate_next_action(self, tools, current_query: str, timeout: int = 10) -> str:

        system_prompt = create_system_prompt(tools)
        """Generate the next action decision based on current state"""
        loop = asyncio.get_event_loop()
        
        # Enhanced prompt with strict formatting requirements
        format_instructions = """
        IMPORTANT: You must respond with EXACTLY ONE action per response using these formats:
        
        1. For function calls:
        FUNCTION_CALL:function_name|param1|param2
        
        2. For PowerPoint operations:
        POWERPOINT:operation|param1|param2
        
        3. For final answers:
        FINAL_ANSWER:your answer here
        
        Rules:
        - Output ONLY ONE command per response
        - Do not include any explanations or additional text
        - Do not use markdown formatting
        - Each response must start with one of the prefixes above
        - Parameters must be separated by single pipe character |
        - No spaces around the colon or pipe characters
        """
        
        enhanced_prompt = (
            system_prompt + 
            "\n\n" + 
            format_instructions + 
            "\n\nExample valid responses:" +
            "\nFUNCTION_CALL:calculate|1|2|3" +
            "\nPOWERPOINT:add_slide|Title" +
            "\nFINAL_ANSWER:The result is 42"
        )
        
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None, 
                lambda: self.client.models.generate_content(
                    model="gemini-2.0-flash-lite",
                    contents=[{
                        "role": "user",
                        "parts": [{"text": f"{enhanced_prompt}\n\nQuery: {current_query}"}]
                    }]
                )
            ),
            timeout=timeout
        )
        
        # Clean up the response to ensure proper formatting
        cleaned_response = self._clean_response(response.text.strip())
        logger.info(f"Generated response for next action: {cleaned_response}")
        return cleaned_response
    
    def _clean_response(self, response: str) -> str:
        """Clean up the response to ensure proper formatting"""
        # Remove any markdown code blocks
        response = response.replace("```", "").strip()
        
        # Get the first line that starts with a valid prefix
        valid_prefixes = ["FUNCTION_CALL:", "POWERPOINT:", "FINAL_ANSWER:"]
        lines = response.split("\n")
        
        for line in lines:
            line = line.strip()
            for prefix in valid_prefixes:
                if line.startswith(prefix):
                    # Remove any extra whitespace around separators
                    parts = line.split(":")
                    if len(parts) > 1:
                        command = parts[0]
                        params = ":".join(parts[1:])
                        params = "|".join(p.strip() for p in params.split("|"))
                        return f"{command}:{params}"
        
        # If no valid format found, return error
        return "FINAL_ANSWER:Error: Invalid response format"
    
    def update_query_state(self, original_query: str, iteration_responses: list) -> str:
        """Update the query state based on previous responses"""
        if not iteration_responses:
            return original_query
        
        # Create a more focused context with results
        context = "\n\nPrevious steps:\n"
        for resp in iteration_responses[-3:]:  # Only show last 3 responses
            if isinstance(resp, dict):
                command = resp.get('command', '')
                result = resp.get('result', None)
                context += f"- Command: {command}\n"
                if result is not None:
                    context += f"  Result: {result}\n"
            else:
                context += f"- {resp}\n"
                
        return f"{original_query}{context}\n\nWhat is the next single action to take?"