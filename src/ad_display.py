import os
import random
import pygame
import pillow_heif
from PIL import Image
import io
import cv2

class AdManager:
    def __init__(self, ads_base_path='.'):
        pygame.init()
        pygame.display.init()
        
        # Get screen dimensions
        screen_info = pygame.display.Info()
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h
        
        # Create fullscreen display
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Smart Advertisement System")
        
        self.ads_base_path = ads_base_path

    def select_ad(self, gender, age):
        """Select an appropriate advertisement based on gender and age"""
        # Extract age value from the age string (e.g., '(25-32)' -> 25)
        age_num = int(age.strip('()').split('-')[0])
        
        # Map the detected age to available age range folders
        age_ranges = {
            (0, 2): '0-2',
            (3, 6): '4-6',
            (7, 12): '8-12',
            (13, 20): '15-20',
            (21, 32): '25-32',
            (33, 43): '38-43',
            (44, 53): '48-53',
            (54, 100): '60-100'
        }
        
        # Find the appropriate age range
        target_range = None
        for (start, end), range_dir in age_ranges.items():
            if start <= age_num <= end:
                target_range = range_dir
                break
        
        if not target_range:
            target_range = '25-32'  # Default age range if no match
        
        # Construct path to specific age category within gender folder
        gender_path = os.path.join(self.ads_base_path, gender.lower())
        age_path = os.path.join(gender_path, target_range)
        
        if not os.path.exists(age_path):
            print(f"No ads found for {gender}, age {target_range}")
            # Fallback to gender folder if age-specific folder doesn't exist
            if os.path.exists(gender_path):
                ad_path = gender_path
            else:
                return None
        else:
            ad_path = age_path

        # Get list of ad files (now including .heic)
        ad_files = [f for f in os.listdir(ad_path) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.gif', '.heic'))]
        
        if not ad_files:
            print(f"No image ads found in {ad_path}")
            return None
        
        # Randomly select an ad
        selected_ad = random.choice(ad_files)
        return os.path.join(ad_path, selected_ad)

    def display_ad(self, ad_path, display_time=5):
        """Display the selected advertisement"""
        if not ad_path:
            return
        
        try:
            # Handle HEIC format
            if ad_path.lower().endswith('.heic'):
                # Read HEIC file
                heif_file = pillow_heif.read_heif(ad_path)
                # Convert to PIL Image
                image = Image.frombytes(
                    heif_file.mode,
                    heif_file.size,
                    heif_file.data,
                    "raw",
                )
                # Convert PIL image to bytes for pygame
                with io.BytesIO() as bio:
                    image.save(bio, format='PNG')
                    bio.seek(0)
                    ad_image = pygame.image.load(bio)
            else:
                # Load non-HEIC image directly
                ad_image = pygame.image.load(ad_path)
            
            # Scale the image
            ad_image = pygame.transform.scale(ad_image, (self.screen_width, self.screen_height))
            
            # Display the ad
            self.screen.blit(ad_image, (0, 0))
            pygame.display.flip()
            
            # Keep displaying until window is closed
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:  # Still allow 'q' to quit
                            running = False
                pygame.time.wait(100)  # Small delay to prevent high CPU usage
            
            # Clear the screen
            self.screen.fill((0, 0, 0))
            pygame.display.flip()
        
        except Exception as e:
            print(f"Error displaying ad: {e}")

    def close(self):
        """Cleanup pygame resources"""
        pygame.quit()
        #mvdk;vnijdqbvuq