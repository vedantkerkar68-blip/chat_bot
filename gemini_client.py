import os
import base64
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import json

# Load environment variables
load_dotenv()

class GeminiClient:
    def __init__(self):
        """Initialize Gemini client with API key from environment variables."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize models (using latest available models)
        self.text_model = genai.GenerativeModel('gemini-2.5-flash')
        self.vision_model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Default parameters
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            max_output_tokens=1500,
            top_p=0.8,
            top_k=40
        )
    
    def get_text_response(self, user_message: str, system_message: str = None) -> Dict[str, Any]:
        """
        Get a response from Gemini for text-based queries.
        
        Args:
            user_message (str): The user's message/query
            system_message (str, optional): System message to set context
            
        Returns:
            Dict containing response, usage info, and success status
        """
        try:
            # Combine system message with user message if provided
            if system_message:
                full_message = f"{system_message}\n\nUser: {user_message}"
            else:
                full_message = user_message
            
            response = self.text_model.generate_content(
                full_message,
                generation_config=self.generation_config
            )
            
            return {
                "success": True,
                "response": response.text,
                "usage": {
                    "prompt_tokens": len(full_message.split()),  # Approximation
                    "completion_tokens": len(response.text.split()) if response.text else 0,
                    "total_tokens": len(full_message.split()) + (len(response.text.split()) if response.text else 0)
                },
                "model": "gemini-2.5-flash",
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "response": f"Sorry, I encountered an error: {str(e)}",
                "usage": None,
                "model": None,
                "error": str(e)
            }
    
    def analyze_image(self, image_path: str, user_question: str = "What do you see in this image?") -> Dict[str, Any]:
        """
        Analyze an image using Gemini Pro Vision.
        
        Args:
            image_path (str): Path to the image file
            user_question (str): Question about the image
            
        Returns:
            Dict containing analysis result, usage info, and success status
        """
        try:
            # Load and validate image
            if not os.path.exists(image_path):
                return {
                    "success": False,
                    "response": "Image file not found",
                    "usage": None,
                    "model": None,
                    "error": "File not found"
                }
            
            # Open image using PIL
            try:
                image = Image.open(image_path)
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
            except Exception as img_error:
                return {
                    "success": False,
                    "response": f"Failed to load image: {str(img_error)}",
                    "usage": None,
                    "model": None,
                    "error": str(img_error)
                }
            
            # Generate content with image and text
            response = self.vision_model.generate_content(
                [user_question, image],
                generation_config=self.generation_config
            )
            
            return {
                "success": True,
                "response": response.text,
                "usage": {
                    "prompt_tokens": len(user_question.split()),  # Approximation
                    "completion_tokens": len(response.text.split()) if response.text else 0,
                    "total_tokens": len(user_question.split()) + (len(response.text.split()) if response.text else 0)
                },
                "model": "gemini-2.5-flash",
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "response": f"Sorry, I couldn't analyze the image: {str(e)}",
                "usage": None,
                "model": None,
                "error": str(e)
            }
    
    def get_conversation_response(self, conversation_history: list, new_message: str) -> Dict[str, Any]:
        """
        Get response considering conversation history.
        
        Args:
            conversation_history (list): List of previous messages
            new_message (str): New user message
            
        Returns:
            Dict containing response and metadata
        """
        try:
            # Build conversation context
            context = "You are a helpful AI assistant. Here's our conversation history:\n\n"
            
            # Add conversation history (limit to last 10 exchanges to avoid token limits)
            for i, msg in enumerate(conversation_history[-20:]):  # Last 20 messages
                if msg["role"] == "user":
                    context += f"User: {msg['content']}\n"
                elif msg["role"] == "assistant":
                    context += f"Assistant: {msg['content']}\n"
            
            # Add current message
            context += f"\nNow respond to: {new_message}"
            
            response = self.text_model.generate_content(
                context,
                generation_config=self.generation_config
            )
            
            return {
                "success": True,
                "response": response.text,
                "usage": {
                    "prompt_tokens": len(context.split()),
                    "completion_tokens": len(response.text.split()) if response.text else 0,
                    "total_tokens": len(context.split()) + (len(response.text.split()) if response.text else 0)
                },
                "model": "gemini-2.5-flash",
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "response": f"Sorry, I encountered an error: {str(e)}",
                "usage": None,
                "model": None,
                "error": str(e)
            }
    
    def update_settings(self, **kwargs):
        """Update Gemini client settings."""
        config_updates = {}
        if 'temperature' in kwargs:
            config_updates['temperature'] = max(0.0, min(1.0, kwargs['temperature']))
        if 'max_tokens' in kwargs:
            config_updates['max_output_tokens'] = max(1, min(2048, kwargs['max_tokens']))
        if 'top_p' in kwargs:
            config_updates['top_p'] = max(0.0, min(1.0, kwargs['top_p']))
        if 'top_k' in kwargs:
            config_updates['top_k'] = max(1, min(40, kwargs['top_k']))
        
        if config_updates:
            self.generation_config = genai.types.GenerationConfig(**config_updates)
    
    def get_available_models(self) -> list:
        """Get list of available Gemini models."""
        try:
            models = genai.list_models()
            return [model.name for model in models if 'generateContent' in model.supported_generation_methods]
        except Exception as e:
            print(f"Error fetching models: {e}")
            return ["gemini-2.5-flash", "gemini-2.5-pro"]
    
    def test_connection(self) -> bool:
        """Test the Gemini API connection."""
        try:
            response = self.get_text_response("Hello, this is a test message.")
            return response["success"]
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current models."""
        try:
            return {
                "text_model": "gemini-2.5-flash",
                "vision_model": "gemini-2.5-flash",
                "provider": "Google AI",
                "api_version": "v1",
                "features": ["text_generation", "image_analysis", "conversation"],
                "generation_config": {
                    "temperature": self.generation_config.temperature,
                    "max_output_tokens": self.generation_config.max_output_tokens,
                    "top_p": self.generation_config.top_p,
                    "top_k": self.generation_config.top_k
                }
            }
        except Exception as e:
            return {"error": str(e)}

# Utility functions for backward compatibility with OpenAI structure
def format_conversation_for_api(conversation_history: list) -> list:
    """
    Format conversation history for Gemini API.
    
    Args:
        conversation_history: List of tuples (user_message, ai_response)
        
    Returns:
        List of formatted messages
    """
    messages = []
    for user_msg, ai_msg in conversation_history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": ai_msg})
    return messages

def validate_image_file(file_path: str) -> bool:
    """
    Validate if file is a supported image format.
    
    Args:
        file_path (str): Path to the image file
        
    Returns:
        bool: True if valid image, False otherwise
    """
    supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    file_extension = os.path.splitext(file_path)[1].lower()
    
    return file_extension in supported_formats and os.path.isfile(file_path)

if __name__ == "__main__":
    # Test the Gemini client
    try:
        client = GeminiClient()
        
        # Test text response
        print("Testing text response...")
        response = client.get_text_response("Hello! How are you today?")
        if response["success"]:
            print(f"AI Response: {response['response']}")
            print(f"Tokens used: {response['usage']['total_tokens']}")
        else:
            print(f"Error: {response['error']}")
        
        # Test connection
        print(f"Connection test: {'Passed' if client.test_connection() else 'Failed'}")
        
        # Show model info
        info = client.get_model_info()
        print(f"Model info: {json.dumps(info, indent=2)}")
        
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        print("Please check your API key in the .env file")