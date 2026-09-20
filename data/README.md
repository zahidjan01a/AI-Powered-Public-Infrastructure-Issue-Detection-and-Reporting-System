# Dataset Documentation & Structure

This directory outlines the data pipeline, sources, class taxonomy, and preparation guidelines for the **AI-Powered Public Infrastructure Issue Detection and Reporting System**.

> [!NOTE]
> Due to GitHub file size limits and repository hygiene, image files under `data/raw/`, `data/processed/`, `dataset/raw/`, and `dataset/processed/` are excluded from version control via `.gitignore`. The complete training pipeline is fully reproducible using the Jupyter notebooks in `notebooks/`.

---

## 1. Class Taxonomy & Integer Encoding

The computer vision model classifies input photographs into four mutually exclusive categories:

| Class Index | Class Label | Description | Visual Characteristics |
| :---: | :---: | :--- | :--- |
| `0` | **`garbage`** | Municipal solid waste accumulation | Discarded plastics, papers, illegal refuse piles, overflowing bins. |
| `1` | **`normal`** | Structurally intact infrastructure | Clear, unblemished pavement, sidewalks, and clean roadside areas. |
| `2` | **`pothole`** | Pavement depression / cavity | Structural roadway asphalt holes exposing subsurface aggregate. |
| `3` | **`road_crack`** | Pavement fissures / ruts | Longitudinal, transverse, or alligator cracking across asphalt. |

---

## 2. Dataset Sourcing & Aggregation

The dataset was aggregated from multi-source public computer vision benchmarks on Kaggle:

1. **Garbage Classification Dataset**: 15,515 images covering diverse domestic, industrial, and street waste.
2. **Pothole Detection Dataset**: 991 annotated real-world images of asphalt road cavities.
3. **Surface Crack Detection Dataset**: 40,000 images divided evenly into:
   - `Positive`: 20,000 images exhibiting distinct asphalt/concrete cracks.
   - `Negative`: 20,000 images of smooth, uncracked road surfaces (utilized for the `normal` class).

### Dataset Breakdown

| Category | Raw Aggregate Count | Balanced Experimental Subset | Subset Role |
| :--- | :---: | :---: | :--- |
| **Normal** | 20,410 | 1,000 | Baseline reference infrastructure |
| **Road Crack** | 20,000 | 1,000 | Preventative maintenance detection |
| **Garbage** | 15,515 | 1,000 | Public sanitation issue detection |
| **Pothole** | 991 | 991 | High-priority safety hazard detection |
| **Total** | **56,916** | **3,991** | |

---

## 3. Data Balancing & Partitioning

To mitigate extreme class imbalance (potholes accounting for only ~1.7% of the total raw pool) and to facilitate efficient convergence under CPU hardware constraints:

- **Stratified Sampling**: 1,000 random images were sampled from each majority class (`garbage`, `normal`, `road_crack`) and combined with all 991 available `pothole` samples, yielding a balanced dataset of **3,991 images**.
- **Data Partitions**:
  - **Training Set (70%)**: 2,793 images (approx. 700 per category)
  - **Validation Set (15%)**: 599 images (approx. 150 per category)
  - **Testing Set (15%)**: 599 images (approx. 150 per category)

---

## 4. Preprocessing & Data Augmentation

All images passed through the following data preparation pipeline:

1. **Color Space Standardization**: Conversion of all images to 3-channel RGB.
2. **Spatial Rescaling**: Resized to $224 \times 224$ pixels using high-fidelity Lanczos interpolation.
3. **Intensity Rescaling**: Pixel values mapped to $[0, 1]$ range (`pixel / 255.0`).
4. **On-the-Fly Training Augmentation**:
   - Rotation: $\pm 20^\circ$
   - Width / Height Shift: up to $20\%$
   - Zoom Range: up to $20\%$
   - Horizontal Flipping: Random $50\%$

---

## 5. How to Reproduce Dataset Extraction

1. Place downloaded dataset archives into `data/raw/` or `dataset/raw/`.
2. Open and run [`notebooks/01_dataset_preparation.ipynb`](../notebooks/01_dataset_preparation.ipynb) to extract files into `data/processed/`.
3. Open and run [`notebooks/02_train_mobilenetv2.ipynb`](../notebooks/02_train_mobilenetv2.ipynb) to assemble DataFrames, balance distributions, and train the model.
