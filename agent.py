import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
from agent.perception import Perception
from agent.decision import Decision
from agent.action import Action
from agent.memory import Memory
import asyncio
from logger_config import logger

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

async def main():
    max_retries = 3
    retry_count = 0
    memory = Memory()
    
    while retry_count < max_retries:
        try:
            logger.info("=== Starting New Attempt ===")
            logger.info(f"Retry count: {retry_count}")
            memory.reset()
            server_params = StdioServerParameters(
                command="python",
                args=["mcp-server.py", "dev"]
            )

            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    try:
                        await session.initialize()
                        logger.info("Session initialized successfully")
                        
                        # Initialize layers
                        perception = Perception(session)
                        decision = Decision(client)
                        action = Action(session)
                        logger.info("Agent layers initialized")
                        
                        # Get tools
                        tools = await perception.get_available_tools()
                        logger.info(f"Available tools loaded: {len(tools)} tools found")
                        
                        query = """Find the ASCII values of characters in NARENDRA and then return sum of exponentials of those values. 
                        Also, create a PowerPoint presentation showing the Final Answer inside a rectangle box."""
                        
                        logger.info("=== Starting Task Execution ===")
                        logger.info(f"Initial Query: {query}")
                        
                        while memory.should_continue():
                            try:
                                logger.info(f"\n--- Iteration {memory.iteration + 1} ---")
                                # Decision phase
                                logger.debug("Step 1: Decision Phase")
                                current_query = decision.update_query_state(query, memory.iteration_responses)
                                logger.debug(f"Updated Query State: {current_query}")
                                
                                response_text = await decision.generate_next_action(tools, current_query)
                                logger.info(f"Generated Action: {response_text}")
                                
                                # Perception phase
                                logger.debug("Step 2: Perception Phase")
                                parsed_response = await perception.parse_response(response_text)
                                logger.debug(f"Parsed Response: {parsed_response}")
                                
                                # Action phase
                                logger.debug("Step 3: Action Phase")
                                result = None
                                if parsed_response["type"] == "function":
                                    logger.info(f"Executing function: {parsed_response['params'][0]}")
                                    result = await action.execute_function(
                                        parsed_response['params'][0],
                                        parsed_response['params'][1:],
                                        tools
                                    )
                                    logger.info(f"Function result: {result}")
                                    
                                    # Store the result in memory for next iteration
                                    memory.store_result(result)
                                
                                    # Update query state with result
                                    current_state = {
                                        'command': response_text,
                                        'result': result
                                    }
                                    memory.update_state(current_state)
                                elif parsed_response["type"] == "powerpoint":
                                    logger.info(f"Executing PowerPoint command: {parsed_response['params'][0]}")
                                    result = await action.execute_function(
                                        parsed_response['params'][0],
                                        parsed_response['params'][1:],
                                        tools
                                    )
                                    logger.info(f"PowerPoint command result: {result}")
                                    current_state = {
                                        'command': response_text,
                                        'result': result
                                    }
                                    memory.update_state(current_state)
                                else:
                                    logger.info(f"No action needed for response type: {parsed_response['type']}")
                                    current_state = {
                                        'command': response_text,
                                        'result': None
                                    }
                                    memory.update_state(current_state)
                                
                                if parsed_response["type"] == "final":
                                    logger.info("Task completed successfully")
                                    return
                                    
                                logger.info(f"Iteration {memory.iteration} completed")
                                
                            except Exception as inner_e:
                                logger.error(f"Error in iteration {memory.iteration}: {inner_e}", exc_info=True)
                                memory.iteration += 1
                                continue
                                
                    except Exception as session_e:
                        logger.error(f"Session error: {session_e}", exc_info=True)
                        raise
                        
            break
        except Exception as e:
            logger.error(f"Attempt {retry_count + 1} failed: {e}", exc_info=True)
            retry_count += 1
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
    
    
