# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from PIL import Image as PILImage
import math
import sys
import time
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# Pydantic models for input/output validation
class NumberInput(BaseModel):
    a: int = Field(..., description="First number")
    b: int = Field(..., description="Second number")

class SingleNumberInput(BaseModel):
    a: int = Field(..., description="Input number")

class ListInput(BaseModel):
    l: List[int] = Field(..., description="List of numbers")

class StringInput(BaseModel):
    string: str = Field(..., description="Input string")

class NumberOutput(BaseModel):
    result: int = Field(..., description="Result of the operation")

class FloatOutput(BaseModel):
    result: float = Field(..., description="Result of the operation")

class ListOutput(BaseModel):
    result: List[int] = Field(..., description="Result list")

class PowerPointResponse(BaseModel):
    content: List[TextContent] = Field(..., description="PowerPoint operation response")

class RectangleInput(BaseModel):
    x1: int = Field(..., ge=1, le=8, description="Starting X coordinate")
    y1: int = Field(..., ge=1, le=8, description="Starting Y coordinate")
    x2: int = Field(..., ge=1, le=8, description="Ending X coordinate")
    y2: int = Field(..., ge=1, le=8, description="Ending Y coordinate")

class ImageInput(BaseModel):
    image_path: str = Field(..., description="Path to the image file")

class ImageOutput(BaseModel):
    data: bytes = Field(..., description="Image data")
    format: str = Field(..., description="Image format")

class FibonacciInput(BaseModel):
    n: int = Field(..., description="Number of Fibonacci numbers to return")

class PowerPointTextInput(BaseModel):
    text: str = Field(..., description="Text to add to the PowerPoint slide")

from pptx import Presentation
from pptx.util import Inches
import os
from pptx.dml.color import RGBColor
from pptx.util import Pt

# instantiate an MCP server client
mcp = FastMCP("Calculator")

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(input: NumberInput) -> NumberOutput:
    """Add two numbers"""
    print("CALLED: add(input: NumberInput) -> NumberOutput:")
    return NumberOutput(result=int(input.a + input.b))

@mcp.tool()
def add_list(input: ListInput) -> NumberOutput:
    """Add all numbers in a list"""
    print("CALLED: add_list(input: ListInput) -> NumberOutput:")
    return NumberOutput(result=sum(input.l))

# subtraction tool
@mcp.tool()
def subtract(input: NumberInput) -> NumberOutput:
    """Subtract two numbers"""
    print("CALLED: subtract(input: NumberInput) -> NumberOutput:")
    return NumberOutput(result=int(input.a - input.b))

# multiplication tool
@mcp.tool()
def multiply(input: NumberInput) -> NumberOutput:
    """Multiply two numbers"""
    print("CALLED: multiply(input: NumberInput) -> NumberOutput:")
    return NumberOutput(result=int(input.a * input.b))

#  division tool
@mcp.tool() 
def divide(input: NumberInput) -> FloatOutput:
    """Divide two numbers"""
    print("CALLED: divide(input: NumberInput) -> FloatOutput:")
    return FloatOutput(result=float(input.a / input.b))

# power tool
@mcp.tool()
def power(input: NumberInput) -> NumberOutput:
    """Power of two numbers"""
    print("CALLED: power(input: NumberInput) -> NumberOutput:")
    return NumberOutput(result=int(input.a ** input.b))

# square root tool
@mcp.tool()
def sqrt(input: SingleNumberInput) -> FloatOutput:
    """Square root of a number"""
    print("CALLED: sqrt(input: SingleNumberInput) -> FloatOutput:")
    return FloatOutput(result=float(input.a ** 0.5))

# cube root tool
@mcp.tool()
def cbrt(input: SingleNumberInput) -> FloatOutput:
    """Cube root of a number"""
    print("CALLED: cbrt(input: SingleNumberInput) -> FloatOutput:")
    return FloatOutput(result=float(input.a ** (1/3)))

# factorial tool
@mcp.tool()
def factorial(input: SingleNumberInput) -> NumberOutput:
    """factorial of a number"""
    print("CALLED: factorial(input: SingleNumberInput) -> NumberOutput:")
    return NumberOutput(result=int(math.factorial(input.a)))

# log tool
@mcp.tool()
def log(input: SingleNumberInput) -> FloatOutput:
    """log of a number"""
    print("CALLED: log(input: SingleNumberInput) -> FloatOutput:")
    return FloatOutput(result=float(math.log(input.a)))

# remainder tool
@mcp.tool()
def remainder(input: NumberInput) -> NumberOutput:
    """remainder of two numbers divison"""
    print("CALLED: remainder(input: NumberInput) -> NumberOutput:")
    return NumberOutput(result=int(input.a % input.b))

# sin tool
@mcp.tool()
def sin(input: SingleNumberInput) -> FloatOutput:
    """sin of a number"""
    print("CALLED: sin(input: SingleNumberInput) -> FloatOutput:")
    return FloatOutput(result=float(math.sin(input.a)))

# cos tool
@mcp.tool()
def cos(input: SingleNumberInput) -> FloatOutput:
    """cos of a number"""
    print("CALLED: cos(input: SingleNumberInput) -> FloatOutput:")
    return FloatOutput(result=float(math.cos(input.a)))

# tan tool
@mcp.tool()
def tan(input: SingleNumberInput) -> FloatOutput:
    """tan of a number"""
    print("CALLED: tan(input: SingleNumberInput) -> FloatOutput:")
    return FloatOutput(result=float(math.tan(input.a)))

# mine tool
@mcp.tool()
def mine(input: NumberInput) -> NumberOutput:
    """special mining tool"""
    print("CALLED: mine(input: NumberInput) -> NumberOutput:")
    return NumberOutput(result=int(input.a - input.b - input.b))

@mcp.tool()
def create_thumbnail(input: ImageInput) -> ImageOutput:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(input: ImageInput) -> ImageOutput:")
    img = PILImage.open(input.image_path)
    img.thumbnail((100, 100))
    return ImageOutput(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(input: StringInput) -> ListOutput:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(input: StringInput) -> ListOutput:")
    return ListOutput(result=[ord(char) for char in input.string])

@mcp.tool()
def int_list_to_exponential_sum(input: ListInput) -> FloatOutput:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(input: ListInput) -> FloatOutput:")
    return FloatOutput(result=sum(math.exp(i) for i in input.l))

@mcp.tool()
def fibonacci_numbers(input: FibonacciInput) -> ListOutput:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(input: FibonacciInput) -> ListOutput:")
    if input.n <= 0:
        return ListOutput(result=[])
    fib_sequence = [0, 1]
    for _ in range(2, input.n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return ListOutput(result=fib_sequence[:input.n])

@mcp.tool()
async def close_powerpoint() -> PowerPointResponse:
    """Close PowerPoint"""
    try:
        os.system('pkill "Microsoft PowerPoint"')
        time.sleep(2)
        
        return PowerPointResponse(
            content=[
                TextContent(
                    type="text",
                    text="PowerPoint closed successfully"
                )
            ]
        )
    except Exception as e:
        print(f"Error in close_powerpoint: {str(e)}")
        return PowerPointResponse(
            content=[
                TextContent(
                    type="text",
                    text=f"Error closing PowerPoint: {str(e)}"
                )
            ]
        )

@mcp.tool()
async def open_powerpoint() -> PowerPointResponse:
    """Open a new PowerPoint presentation"""
    try:
        await close_powerpoint()
        time.sleep(3)
        
        prs = Presentation()
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)
        
        filename = 'presentation.pptx'
        prs.save(filename)
        time.sleep(5)
        
        os.system(f'open "{filename}"')
        time.sleep(10)
        
        return PowerPointResponse(
            content=[
                TextContent(
                    type="text",
                    text="PowerPoint opened successfully with a new presentation"
                )
            ]
        )
    except Exception as e:
        print(f"Error in open_powerpoint: {str(e)}")
        return PowerPointResponse(
            content=[
                TextContent(
                    type="text",
                    text=f"Error opening PowerPoint: {str(e)}"
                )
            ]
        )

@mcp.tool()
async def draw_rectangle(input: RectangleInput) -> PowerPointResponse:
    """Draw a rectangle in the first slide of PowerPoint"""
    try:
        print(f"[MCP Tool] Drawing rectangle with parameters: {input}")
        
        # Validate coordinates
        if input.x2 <= input.x1 or input.y2 <= input.y1:
            error_msg = f"End coordinates must be greater than start coordinates"
            print(f"{error_msg}")
            return PowerPointResponse(
                content=[TextContent(type="text", text=error_msg)]
            )

        # Wait before modifying the presentation
        time.sleep(2)
        
        # Ensure PowerPoint is closed before modifying the file
        await close_powerpoint()
        time.sleep(2)
        
        prs = Presentation('presentation.pptx')
        slide = prs.slides[0]
        
        # Convert coordinates to inches
        left = Inches(input.x1)
        top = Inches(input.y1)
        width = Inches(input.x2 - input.x1)
        height = Inches(input.y2 - input.y1)
        
        # Add rectangle
        shape = slide.shapes.add_shape(
            1,  # MSO_SHAPE.RECTANGLE
            left, top, width, height
        )
        
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        shape.line.color.rgb = RGBColor(0, 0, 0)
        shape.line.width = Pt(4)
        
        prs.save('presentation.pptx')
        time.sleep(2)
        
        os.system('open presentation.pptx')
        time.sleep(5)
        
        return PowerPointResponse(
            content=[
                TextContent(
                    type="text",
                    text=f"Rectangle drawn successfully from ({input.x1},{input.y1}) to ({input.x2},{input.y2})"
                )
            ]
        )
            
    except Exception as e:
        error_msg = f"Error in draw_rectangle: {str(e)}"
        print(f"{error_msg}")
        return PowerPointResponse(
            content=[TextContent(type="text", text=error_msg)]
        )

@mcp.tool()
async def add_text_in_powerpoint(input: PowerPointTextInput) -> PowerPointResponse:
    """Add text to the first slide of PowerPoint"""
    try:
        print(f"[MCP Tool] Received text to add: {input.text}")
        
        await close_powerpoint()
        time.sleep(5)
        
        prs = Presentation('presentation.pptx')
        slide = prs.slides[0]
        
        left = Inches(2.2)
        top = Inches(2.5)
        width = Inches(4.6)
        height = Inches(2)
        
        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame
        text_frame.clear()
        text_frame.word_wrap = True
        text_frame.vertical_anchor = 1
        
        lines = input.text.split('\n')
        
        for line in lines:
            if line.strip():
                p = text_frame.add_paragraph()
                p.text = line.strip()
                p.alignment = 1
                
                run = p.runs[0]
                if "Final Result:" in line:
                    run.font.size = Pt(32)
                    run.font.bold = True
                else:
                    run.font.size = Pt(28)
                    run.font.bold = True
                
                run.font.color.rgb = RGBColor(0, 0, 0)
                p.space_after = Pt(12)
        
        prs.save('presentation.pptx')
        time.sleep(5)
        
        os.system('open presentation.pptx')
        time.sleep(5)
        
        return PowerPointResponse(
            content=[
                TextContent(
                    type="text",
                    text=f"Text added successfully: {input.text}"
                )
            ]
        )
    except Exception as e:
        print(f"Error in add_text_in_powerpoint: {str(e)}")
        return PowerPointResponse(
            content=[
                TextContent(
                    type="text",
                    text=f"Error adding text: {str(e)}"
                )
            ]
        )

# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING THE SERVER")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
