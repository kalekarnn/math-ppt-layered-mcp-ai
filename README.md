# Math PowerPoint Plan Reason MCP AI
This project implements an intelligent agent system that combines mathematical calculations with PowerPoint presentation generation using a multi-layer architecture. The system demonstrates advanced planning and reasoning capabilities through its modular design.


## Architecture Overview
The system is built on a layered architecture consisting of four main components:

### 1. Perception Layer
- Implemented in `perception.py`
- Responsible for:
  - Perceiving available tools from the environment
  - Parsing and understanding responses from the LLM
  - Converting raw input into structured data for decision making

### 2. Decision Layer
- Implemented in `decision.py`
- Handles:
  - Generation of next actions based on current state
  - Integration with Google's Gemini AI model
  - Response formatting and cleaning
  - Query state management

### 3. Action Layer
- Implemented in `action.py`
- Manages:
  - Execution of function calls
  - Parameter preparation and validation
  - Tool interaction and response handling
  - PowerPoint operations

### 4. Memory Layer
- Implemented in `memory.py`
- Maintains:
  - Iteration state
  - Response history
  - Result storage
  - Execution flow control


## Key Features
1. Mathematical Operations
   
   - Basic arithmetic operations (add, subtract, multiply, divide)
   - Advanced functions (power, square root, cube root)
   - Trigonometric functions (sin, cos, tan)
   - Special operations (factorial, logarithm)

2. String Processing
   
   - ASCII value conversion
   - Character manipulation
   - List operations

3. PowerPoint Integration
   
   - Slide creation and management
   - Shape drawing (rectangles)
   - Text insertion
   - Presentation formatting

4. Error Handling & Retry Mechanism
   
   - Robust error handling at multiple levels
   - Retry system for failed operations
   - Graceful degradation


## System Flow
1. Initialization
   
   - Environment setup
   - Tool discovery
   - Layer initialization

2. Execution Cycle
   
   - Query processing
   - Decision generation
   - Action execution
   - State update
   - Result storage

3. Memory Management
   
   - State tracking
   - History maintenance
   - Iteration control


## Requirements
- Python 3.13 or higher
- Dependencies:
  - fastmcp >= 2.2.5
  - google-genai >= 1.12.1
  - mcp >= 1.6.0
  - numpy >= 2.2.5
  - pillow >= 11.2.1
  - python-dotenv >= 1.1.0
  - python-pptx >= 1.0.2


## Setup and Usage

1. Set up environment variables:
- Create a .env file
- Add your Gemini API key: GEMINI_API_KEY=your_api_key_here

2. Run the application:
```
uv run agent.py
```

## Logging
The system uses a comprehensive logging system (configured in `logger_config.py` ) that provides:

- Multiple log levels (INFO, DEBUG, ERROR)
- Console and file output
- Emoji-enhanced formatting
- Rotating file handler
This architecture enables complex task execution while maintaining modularity, extensibility, and robust error handling.
