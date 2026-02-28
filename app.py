import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

st.set_page_config(layout="wide")
st.title("Three-Segment Piecewise Contrast Stretching")

# -----------------------------
# Upload Image
# -----------------------------
uploaded_file = st.file_uploader("Upload Grayscale Image", type=["jpg","png","jpeg"])

if uploaded_file is not None:

    # Read image
    image = Image.open(uploaded_file).convert("L")
    img = np.array(image, dtype=np.float32)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(image)

    # -----------------------------
    # Sidebar Parameters
    # -----------------------------
    st.sidebar.header("Adjust Parameters")

    r1 = st.sidebar.slider("a (Lower Breakpoint)", 1, 254, 70)
    r2 = st.sidebar.slider("b (Upper Breakpoint)", r1+1, 255, 140)

    s1 = st.sidebar.slider("va (Output at a)", 0, 255, 30)
    s2 = st.sidebar.slider("vb (Output at b)", 0, 255, 200)

    # -----------------------------
    # Calculate Slopes
    # -----------------------------
    alpha = s1 / r1
    beta = (s2 - s1) / (r2 - r1)
    gamma = (255 - s2) / (255 - r2)

    st.sidebar.subheader("Slopes")
    st.sidebar.write("α =", round(alpha,3))
    st.sidebar.write("β =", round(beta,3))
    st.sidebar.write("γ =", round(gamma,3))

    # -----------------------------
    # Apply Piecewise Transformation
    # -----------------------------
    output = np.zeros_like(img)

    output[img < r1] = alpha * img[img < r1]

    mask2 = (img >= r1) & (img < r2)
    output[mask2] = beta * (img[mask2] - r1) + s1

    output[img >= r2] = gamma * (img[img >= r2] - r2) + s2

    output = np.clip(output, 0, 255).astype(np.uint8)

    with col2:
        st.subheader("Enhanced Image")
        st.image(output)

    # -----------------------------
    # Transformation Graph
    # -----------------------------
    st.subheader("Piecewise Linear Transformation Graph")

    fig1, ax1 = plt.subplots()

    ax1.plot([0, r1], [0, s1])
    ax1.plot([r1, r2], [s1, s2])
    ax1.plot([r2, 255], [s2, 255])

    ax1.axvline(r1, linestyle="--")
    ax1.axvline(r2, linestyle="--")
    ax1.axhline(s1, linestyle="--")
    ax1.axhline(s2, linestyle="--")

    ax1.text(r1/2, s1/2, "α", fontsize=14)
    ax1.text((r1+r2)/2, (s1+s2)/2, "β", fontsize=14)
    ax1.text((r2+255)/2, (s2+255)/2, "γ", fontsize=14)

    ax1.set_xlim(0,255)
    ax1.set_ylim(0,255)
    ax1.set_xlabel("Input Intensity (u)")
    ax1.set_ylabel("Output Intensity (v)")
    ax1.set_title("Contrast Stretching Function")

    st.pyplot(fig1)

    # -----------------------------
    # GRID VISUALIZATION
    # -----------------------------
    st.subheader("Input and Output Pixel Grid (10x10)")

    grid_size = 10
    input_grid = img[:grid_size, :grid_size]
    output_grid = output[:grid_size, :grid_size]

    x_coord = st.slider("Select X (Top → Bottom)", 0, grid_size-1, 5, key="x_slider")
    y_coord = st.slider("Select Y (Left → Right)", 0, grid_size-1, 5, key="y_slider")

    st.write(f"Selected Pixel Coordinate: (x={x_coord}, y={y_coord})")
    st.write(f"Input Pixel Value: {int(input_grid[x_coord, y_coord])}")
    st.write(f"Output Pixel Value: {int(output_grid[x_coord, y_coord])}")

    col3, col4 = st.columns(2)

    # -------- INPUT GRID --------
    with col3:
        st.write("Input Grid")

        fig2, ax2 = plt.subplots()
        ax2.imshow(input_grid, cmap="gray")

        ax2.set_xticks(np.arange(-0.5, grid_size, 1), minor=True)
        ax2.set_yticks(np.arange(-0.5, grid_size, 1), minor=True)
        ax2.grid(which="minor", color="black", linestyle='-', linewidth=0.5)

        # Add pixel values as text
        for i in range(grid_size):
            for j in range(grid_size):
                pixel_val = int(input_grid[i, j])
                ax2.text(j, i, str(pixel_val), ha="center", va="center",
                        color="white" if pixel_val < 128 else "black", fontsize=8)

        ax2.add_patch(plt.Rectangle((y_coord-0.5, x_coord-0.5),
                                    1, 1,
                                    edgecolor='red',
                                    facecolor='none',
                                    linewidth=2))

        ax2.set_xlabel("Y (Left → Right)")
        ax2.set_ylabel("X (Top → Bottom)")
        ax2.set_ylim(grid_size-0.5, -0.5)

        st.pyplot(fig2)

    # -------- OUTPUT GRID --------
    with col4:
        st.write("Output Grid")

        fig3, ax3 = plt.subplots()
        ax3.imshow(output_grid, cmap="gray")

        ax3.set_xticks(np.arange(-0.5, grid_size, 1), minor=True)
        ax3.set_yticks(np.arange(-0.5, grid_size, 1), minor=True)
        ax3.grid(which="minor", color="black", linestyle='-', linewidth=0.5)

        # Add pixel values as text
        for i in range(grid_size):
            for j in range(grid_size):
                pixel_val = int(output_grid[i, j])
                ax3.text(j, i, str(pixel_val), ha="center", va="center",
                        color="white" if pixel_val < 128 else "black", fontsize=8)

        ax3.add_patch(plt.Rectangle((y_coord-0.5, x_coord-0.5),
                                    1, 1,
                                    edgecolor='red',
                                    facecolor='none',
                                    linewidth=2))

        ax3.set_xlabel("Y (Left → Right)")
        ax3.set_ylabel("X (Top → Bottom)")
        ax3.set_ylim(grid_size-0.5, -0.5)

        st.pyplot(fig3)

    # -----------------------------
    # Download Enhanced Image
    # -----------------------------
    st.subheader("Download Enhanced Image")

    result_image = Image.fromarray(output)
    buffer = BytesIO()
    result_image.save(buffer, format="PNG")

    st.download_button(
        label="Download Image",
        data=buffer.getvalue(),
        file_name="enhanced_image.png",
        mime="image/png"
    )