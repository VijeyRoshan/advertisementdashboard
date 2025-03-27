import os
import shutil

def organize_ads(source_dir, dest_base_dir):
    # Ensure destination directory exists
    os.makedirs(dest_base_dir, exist_ok=True)
    
    # Get all image files in the source directory
    image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.gif'))]
    
    # List to track organized images
    organized_images = []
    
    # Copy files to the destination directory
    for filename in image_files:
        src_path = os.path.join(source_dir, filename)
        dest_path = os.path.join(dest_base_dir, filename)
        
        # Copy the file
        shutil.copy2(src_path, dest_path)
        organized_images.append(filename)
        print(f"Copied {filename} to {dest_path}")
    
    return organized_images

def main():
    # Source directory containing images
    source_directory = 'Example'
    
    # Destination directories
    male_ads_directory = os.path.join('src', 'male')
    female_ads_directory = os.path.join('src', 'female')
    
    # Organize ads for males
    print("\nOrganizing Male Advertisements:")
    male_images = organize_ads(source_directory, male_ads_directory)
    
    # Organize ads for females
    print("\nOrganizing Female Advertisements:")
    female_images = organize_ads(source_directory, female_ads_directory)
    
    # Print summary
    print("\nOrganization Summary:")
    print(f"Total images organized: {len(male_images) + len(female_images)}")
    print(f"Male ads: {len(male_images)}")
    print(f"Female ads: {len(female_images)}")

if __name__ == "__main__":
    main()