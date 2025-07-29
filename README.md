# StrechFlow
StretchFlow is a real-time pose analysis system that detects and tracks stretching movements using MediaPipe and OpenCV. Designed for fitness, wellness, and ergonomic use cases, StretchFlow provides immediate visual and auditory feedback to help users perform stretches correctly and safely.

## Instalation

### Option 1: Local Setup with Conda

#### 1. Create and Activate Conda

```bash
conda create -n stretchflow python=3.11 -y
conda activate stretchflow
```

Navigate to the project directory (where the `requirements.txt` is located) and install the dependencies:

#### 2. Install dependencies

```bash
pip install -r requirements.txt
```

#### 3. Run the app

```bash
python app/main.py
```

### Option 2: Run with Docker

#### 1. Build the Docker Image

Navigate to the project directory (where the `Dockerfile` is located) and build the Docker image:

```bash
docker build -t stretchflow .
```

#### 2. Run the Docker Container

Run the container, ensuring it has access to your local display for `cv2.imshow`:

```bash
docker run -it --rm \
    --device=/dev/video0 \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "$(pwd)":/app \
    stretchflow
```

#### Notes:
- The `-e DISPLAY=$DISPLAY` and `-v /tmp/.X11-unix:/tmp/.X11-unix` options allow the container to access your local display for GUI applications like `cv2.imshow`.
- If you encounter issues with permissions, you may need to allow access to your X server:
  ```bash
  xhost +local:docker
  ```
  After running the container, you can revoke access with:
  ```bash
  xhost -local:docker
  ```

#### 3. Stop the Container

To stop the container, press `Ctrl+C` in the terminal where the container is running.


This addition provides clear instructions for running the application using Docker while ensuring compatibility with GUI-based features like `cv2.imshow`.This addition provides clear instructions for running the application using Docker while ensuring compatibility with GUI-based features like `cv2.imshow`.

