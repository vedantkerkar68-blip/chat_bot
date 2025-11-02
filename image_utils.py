import cv2
import os
import tempfile
from PIL import Image, ImageTk
import numpy as np
from typing import Optional, Tuple
import tkinter as tk
from datetime import datetime

class ImageProcessor:
    def __init__(self):
        """Initialize image processor with default settings."""
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']
        self.max_image_size = (1024, 1024)  # Max size for processing
        self.temp_dir = tempfile.gettempdir()
    
    def capture_from_camera(self, save_path: str = None) -> Optional[str]:
        """
        Capture image from default camera.
        
        Args:
            save_path (str, optional): Path to save the captured image
            
        Returns:
            str: Path to saved image or None if capture failed
        """
        try:
            # Initialize camera
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                print("Error: Could not open camera")
                return None
            
            # Set camera properties for better quality
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
            print("Press SPACE to capture image or ESC to cancel")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture frame")
                    break
                
                # Display the frame
                cv2.imshow('Camera - Press SPACE to capture, ESC to cancel', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == 32:  # Space key
                    # Generate filename if not provided
                    if not save_path:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        save_path = os.path.join(self.temp_dir, f"camera_capture_{timestamp}.jpg")
                    
                    # Save the captured frame
                    cv2.imwrite(save_path, frame)
                    print(f"Image captured and saved to: {save_path}")
                    break
                elif key == 27:  # ESC key
                    print("Capture cancelled")
                    save_path = None
                    break
            
            # Release camera and close windows
            cap.release()
            cv2.destroyAllWindows()
            
            return save_path
            
        except Exception as e:
            print(f"Error capturing image: {e}")
            return None
    
    def capture_from_camera_headless(self, save_path: str = None) -> Optional[str]:
        """
        Capture image from camera without GUI (for web apps).
        
        Args:
            save_path (str, optional): Path to save the captured image
            
        Returns:
            str: Path to saved image or None if capture failed
        """
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                print("Error: Could not open camera")
                return None
            
            # Set camera properties
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
            # Wait a moment for camera to adjust
            for _ in range(5):
                ret, frame = cap.read()
                if not ret:
                    continue
            
            # Capture the final frame
            ret, frame = cap.read()
            if ret:
                if not save_path:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    save_path = os.path.join(self.temp_dir, f"camera_capture_{timestamp}.jpg")
                
                cv2.imwrite(save_path, frame)
                print(f"Image captured and saved to: {save_path}")
            else:
                save_path = None
                print("Failed to capture image")
            
            cap.release()
            return save_path
            
        except Exception as e:
            print(f"Error capturing image: {e}")
            return None
    
    def validate_image(self, image_path: str) -> bool:
        """
        Validate if the file is a supported image format.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not os.path.isfile(image_path):
            return False
        
        file_extension = os.path.splitext(image_path)[1].lower()
        return file_extension in self.supported_formats
    
    def resize_image(self, image_path: str, max_size: Tuple[int, int] = None) -> str:
        """
        Resize image to fit within maximum dimensions while maintaining aspect ratio.
        
        Args:
            image_path (str): Path to the original image
            max_size (tuple, optional): Maximum (width, height)
            
        Returns:
            str: Path to resized image
        """
        if not max_size:
            max_size = self.max_image_size
        
        try:
            with Image.open(image_path) as img:
                # Calculate new size maintaining aspect ratio
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Create output path
                filename, ext = os.path.splitext(image_path)
                output_path = f"{filename}_resized{ext}"
                
                # Save resized image
                img.save(output_path, quality=95)
                
                return output_path
                
        except Exception as e:
            print(f"Error resizing image: {e}")
            return image_path
    
    def convert_to_rgb(self, image_path: str) -> str:
        """
        Convert image to RGB format (useful for some AI models).
        
        Args:
            image_path (str): Path to the original image
            
        Returns:
            str: Path to converted image
        """
        try:
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                    
                    filename, _ = os.path.splitext(image_path)
                    output_path = f"{filename}_rgb.jpg"
                    
                    img.save(output_path, 'JPEG', quality=95)
                    return output_path
                
                return image_path
                
        except Exception as e:
            print(f"Error converting image: {e}")
            return image_path
    
    def create_thumbnail(self, image_path: str, size: Tuple[int, int] = (150, 150)) -> str:
        """
        Create a thumbnail of the image.
        
        Args:
            image_path (str): Path to the original image
            size (tuple): Thumbnail size (width, height)
            
        Returns:
            str: Path to thumbnail image
        """
        try:
            with Image.open(image_path) as img:
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                filename, ext = os.path.splitext(image_path)
                thumb_path = f"{filename}_thumb{ext}"
                
                img.save(thumb_path, quality=95)
                
                return thumb_path
                
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return image_path
    
    def get_image_info(self, image_path: str) -> dict:
        """
        Get information about the image.
        
        Args:
            image_path (str): Path to the image
            
        Returns:
            dict: Image information
        """
        try:
            with Image.open(image_path) as img:
                return {
                    'filename': os.path.basename(image_path),
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height,
                    'file_size': os.path.getsize(image_path)
                }
                
        except Exception as e:
            print(f"Error getting image info: {e}")
            return {}
    
    def prepare_for_ai_analysis(self, image_path: str) -> str:
        """
        Prepare image for AI analysis by optimizing size and format.
        
        Args:
            image_path (str): Path to the original image
            
        Returns:
            str: Path to prepared image
        """
        if not self.validate_image(image_path):
            raise ValueError("Invalid image file")
        
        # Convert to RGB if needed
        rgb_path = self.convert_to_rgb(image_path)
        
        # Resize if too large
        info = self.get_image_info(rgb_path)
        if info.get('width', 0) > self.max_image_size[0] or info.get('height', 0) > self.max_image_size[1]:
            rgb_path = self.resize_image(rgb_path)
        
        return rgb_path
    
    def cleanup_temp_files(self, file_paths: list):
        """
        Clean up temporary files.
        
        Args:
            file_paths (list): List of file paths to delete
        """
        for file_path in file_paths:
            try:
                if os.path.exists(file_path) and self.temp_dir in file_path:
                    os.remove(file_path)
                    print(f"Cleaned up: {file_path}")
            except Exception as e:
                print(f"Error cleaning up {file_path}: {e}")

class CameraManager:
    def __init__(self):
        """Initialize camera manager."""
        self.camera_available = self.check_camera_availability()
    
    def check_camera_availability(self) -> bool:
        """Check if camera is available."""
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                cap.release()
                return True
            return False
        except Exception:
            return False
    
    def get_camera_list(self) -> list:
        """Get list of available cameras."""
        cameras = []
        for i in range(5):  # Check first 5 camera indices
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    cameras.append(i)
                    cap.release()
            except Exception:
                continue
        return cameras
    
    def test_camera(self, camera_index: int = 0) -> bool:
        """Test if specific camera works."""
        try:
            cap = cv2.VideoCapture(camera_index)
            ret, frame = cap.read()
            cap.release()
            return ret and frame is not None
        except Exception:
            return False

# Utility functions for Tkinter integration
def pil_to_tkinter(pil_image, size=None):
    """Convert PIL image to Tkinter PhotoImage."""
    if size:
        pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(pil_image)

def load_image_for_display(image_path: str, size: Tuple[int, int] = (300, 300)):
    """Load and resize image for display in GUI."""
    try:
        with Image.open(image_path) as img:
            # Calculate size maintaining aspect ratio
            img.thumbnail(size, Image.Resampling.LANCZOS)
            return pil_to_tkinter(img)
    except Exception as e:
        print(f"Error loading image for display: {e}")
        return None

if __name__ == "__main__":
    # Test the image processing functionality
    processor = ImageProcessor()
    camera_mgr = CameraManager()
    
    print(f"Camera available: {camera_mgr.camera_available}")
    print(f"Available cameras: {camera_mgr.get_camera_list()}")
    
    # Test camera capture (uncomment to test)
    # captured_path = processor.capture_from_camera()
    # if captured_path:
    #     print(f"Image captured: {captured_path}")
    #     info = processor.get_image_info(captured_path)
    #     print(f"Image info: {info}")