import os
import json
from crewai.tools import tool

@tool("Image url extract tool")
def image_fetch_tool(doc_path: str) -> str:
    """Tool to extract image url from json file."""
    tool_output = "Design Reference Images:\n\n"
    try:
        work_dir = os.getenv("WORK_DIR")
        with open(f"{work_dir}/{doc_path}", 'r') as file:
            _json = json.load(file)
            
        _images = _json.get('design_reference_images', [])
        formatted = "Design Reference Images:\n\n"
        for _image in _images:
            tool_output += f"""
                title: {_image['title']}
                url: {_image['url']}
                -------------------"""
    except Exception as e:
        raise ValueError(f"Failed to fetch space news: {str(e)}")
    #
    return tool_output

#result = image_fetch_tool(f"docs/json/designs-research.json")
#print(result)