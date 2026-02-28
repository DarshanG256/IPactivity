# IPactivity

# Piecewise Linear Image Transformation using Streamlit

## 📌 Project Overview

This project demonstrates **Piecewise Linear Intensity Transformation** in Digital Image Processing using **Python and Streamlit**.

The application allows users to:

- Upload a grayscale image
- Apply piecewise linear contrast transformation
- View original and transformed images
- Display pixel intensity values in a 10×10 grid format
- Compare input and output pixel matrices side-by-side

---

## 🧠 Concept Used

Piecewise Linear Transformation enhances image contrast by dividing intensity values into regions:

For each pixel intensity `r`:

- If `r < a` → `s = αr`
- If `a ≤ r < b` → `s = β(r − a) + αa`
- If `r ≥ b` → `s = γ(r − b) + β(b − a) + αa`

Where:
- `a`, `b` → Intensity breakpoints  
- `α`, `β`, `γ` → Slopes controlling contrast  

---

## 🛠 Technologies Used

- Python
- Streamlit
- NumPy
- Matplotlib
- Pillow (PIL)

⚠ OpenCV is NOT used to avoid system dependency issues (like `libGL.so.1` error).

---

## 🚀 How to Run the Project

### 1️⃣ Install Required Libraries

```bash
pip install streamlit numpy matplotlib pillo  '''

 # To run
streamlit run app.py
