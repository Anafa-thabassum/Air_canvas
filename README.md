# 🎨 Air Canvas – Virtual Drawing using OpenCV

Air Canvas is a computer vision project that allows users to draw in the air using a colored object tracked through a webcam. The application detects the object's movement and converts it into digital drawing strokes on a virtual canvas.

This project demonstrates the use of **OpenCV, NumPy, and computer vision techniques** such as color detection, contour tracking, and real-time video processing.

---

## 🚀 Features

* Draw in the air using a colored object
* Real-time color detection using HSV color space
* Multiple drawing colors
* Clear canvas option
* Live webcam tracking
* Adjustable HSV color detection using sliders
* Smooth drawing using contour tracking

---

## 🛠️ Technologies Used

* **Python**
* **OpenCV**
* **NumPy**
* **Deque (collections)**

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/air-canvas.git
cd air-canvas
```

### 2️⃣ Create a virtual environment

```bash
python3 -m venv venv
```

Activate it:

Mac / Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install opencv-python numpy
```

---

## ▶️ Running the Application

Run the program using:

```bash
python Air-canvas.py
```

Press **Q** to exit the application.

---

## 🎮 How to Use

1. Hold a **colored object** (marker cap, tape, or colored paper).
2. Adjust the **HSV sliders** until only the object appears white in the mask window.
3. Move the object in front of the camera to draw.
4. Use the buttons at the top to change colors or clear the canvas.

Available buttons:

| Button | Action            |
| ------ | ----------------- |
| CLEAR  | Clears the canvas |
| BLUE   | Draw in blue      |
| GREEN  | Draw in green     |
| RED    | Draw in red       |
| YELLOW | Draw in yellow    |

---

## 🧠 How It Works

1. The webcam captures real-time video.
2. Frames are converted from **BGR to HSV color space**.
3. A **color mask** isolates the chosen object.
4. **Contours** are detected from the mask.
5. The object's center position is tracked.
6. The tracked positions are used to draw lines on the canvas.

---

## 📂 Project Structure

```
Air-Canvas/
│
├── Air-canvas.py
├── README.md
└── requirements.txt (optional)
```

---

## 🔮 Future Improvements

Possible enhancements for this project:

* Hand tracking instead of colored marker
* Save drawings as images
* Undo / redo functionality
* Eraser mode
* Gesture-based controls

---

## 📸 Demo

You can draw in the air using a colored object and see the strokes appear on the virtual canvas in real time.

---

## 👩‍💻 Author

Anafa Sadiq


---

## ⭐ If you like this project

Give the repository a star ⭐ and feel free to contribute!
