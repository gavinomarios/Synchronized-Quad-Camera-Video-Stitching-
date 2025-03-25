import cv2
import arducam_mipicamera as arducam
import v4l2  # Used for camera controls
import numpy as np

# Configuration: choose resolution mode for the quad camera.
USE_FULL_RES = False  # True for 4608x2592 (max resolution, lower FPS), False for 2304x1296 (higher FPS).

# Initialize Arducam quad camera
camera = arducam.mipi_camera()
try:
    print("Opening quad camera...")
    camera.init_camera()
    # Select resolution: attempt full or half based on USE_FULL_RES
    if USE_FULL_RES:
        desired_width, desired_height = 4608, 2592
    else:
        desired_width, desired_height = 2304, 1296
    fmt = camera.set_resolution(desired_width, desired_height)
    width, height = fmt[0], fmt[1]
    print(f"Camera resolution set to {width}x{height}")
    if (width, height) != (desired_width, desired_height):
        print("Warning: Desired resolution not supported, using closest match.")
    # Enable auto exposure and white balance (if supported)
    try:
        camera.software_auto_exposure(enable=True)
        camera.software_auto_white_balance(enable=True)
    except Exception as e:
        print("Auto exposure/white balance not supported:", e)
    
    # Prepare OpenCV window
    cv2.namedWindow("Panorama", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Panorama", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    # Calculate half width/height for splitting the mosaic into quadrants
    half_w, half_h = width // 2, height // 2

    print("Starting video loop. Press Esc to exit...")
    while True:
        # Capture a frame in YUV I420 format for fast processing&#8203;:contentReference[oaicite:5]{index=5}
        frame = camera.capture(encoding='i420')
        if frame is None:
            # If capture failed, break out
            print("Capture failed, exiting loop.")
            break
        # Convert the YUV420 image to a BGR (OpenCV) image
        # The frame data is a byte array; first, reshape it to match YUV420 planar layout
        yuv_image = frame.as_array.reshape(int(1.5 * height), int(np.ceil(width / 32.0) * 32))  # align stride to 32
        bgr_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR_I420)
        # Release the frame buffer (free memory)
        del frame

        # Split the mosaic into four sub-images (quadrants)
        cam0 = bgr_image[0:half_h, 0:half_w]        # top-left quadrant
        cam1 = bgr_image[0:half_h, half_w:width]    # top-right quadrant
        cam2 = bgr_image[half_h:height, 0:half_w]   # bottom-left quadrant
        cam3 = bgr_image[half_h:height, half_w:width]  # bottom-right quadrant

        # Optional: apply fixed cropping/translation for alignment (if needed)
        # e.g., crop 20 pixels from overlapping edges:
        # cam0 = cam0[:, :-20]   # crop right edge of cam0 view
        # cam1 = cam1[:, 20:]    # crop left edge of cam1 view
        # (Add similar adjustments for cam2, cam3 if required)

        # Stitch the four views horizontally into a panorama.
        # Adjust the order of cams here depending on actual orientation of cameras.
        # Assuming a clockwise arrangement: cam0 = front, cam1 = right, cam3 = back, cam2 = left.
        panorama = cv2.hconcat([cam0, cam1, cam3, cam2])

        # Display the panoramic view
        cv2.imshow("Panorama", panorama)
        # Check for exit keys
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key
            break
        # Also break if the window is closed by the user
        if cv2.getWindowProperty("Panorama", cv2.WND_PROP_VISIBLE) < 1:
            break

    # End of loop: cleanup
    print("Exiting video loop...")
finally:
    # Release resources
    try:
        camera.close_camera()
    except:
        pass
    cv2.destroyAllWindows()
    print("Camera closed and window destroyed.")
