import cv2
import numpy as np

def create_float_image(width, height):
    # Create a random float image for demonstration
    return (np.random.rand(height, width)*10).astype(np.float32)

def main():
    # Specify video properties
    width, height = 640, 480
    fps = 30
    seconds = 10
    output_path = 'output.avi'

    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Generate and write frames to the video
    for _ in range(fps * seconds):
        # Create a random float image
        frame = create_float_image(width, height)

        # Scale the image values to the 0-255 range for display
        frame = (frame * 255).astype(np.uint8)

        # Write the frame to the video file
        out.write(frame)

    # Release the VideoWriter object
    out.release()

    print(f"Video saved to {output_path}")

if __name__ == "__main__":
    main()
