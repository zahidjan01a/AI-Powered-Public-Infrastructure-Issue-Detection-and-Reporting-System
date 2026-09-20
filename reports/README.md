# Project Evaluation Reports & Presentation

This directory references the technical reports, presentation slide deck, and evaluation summaries for the **AI-Powered Public Infrastructure Issue Detection and Reporting System**.

---

## 1. Project Presentation

The primary slide deck for stakeholders, academic evaluation, and project defense is located at:
- **Presentation File**: [`../presentation/AI_Public_Infrastructure_Detector.pptx`](../presentation/AI_Public_Infrastructure_Detector.pptx)
- **Slide Breakdown**:
  - **Slide 1**: Title, Author (*Zahid Jan, University of Engineering and Technology, Mardan*), and Project Focus (*Vision + Real-Time LLM Municipal Reporting*).
  - **Slide 2**: Problem Statement (Potholes, Road Cracks, Garbage Accumulation, and manual inspection bottlenecks).
  - **Slide 3**: Project Objectives (Computer Vision + Real-Time LLM + 1-Click Department Submission).
  - **Slide 4 & 5**: Dataset Sourcing (56,916 raw images), Class Imbalance, and Data Preparation.
  - **Slide 6**: MobileNetV2 Transfer Learning Architecture (Frozen base, GAP, Dense 128, Dropout 0.3, Dense 4 Softmax).
  - **Slide 7 & 8**: Training Results (98.33% Test Accuracy) and Confusion Matrix Analysis.
  - **Slide 9**: Visual 5-Step Citizen Journey: `Snap Photo & Location` $\rightarrow$ `Smart Preprocessing` $\rightarrow$ `AI Vision` $\rightarrow$ `Dept Routing & SLA` $\rightarrow$ `Live Gemini Report` $\rightarrow$ `1-Click Submit & Ticket ID`.
  - **Slide 10**: Categorical Prediction Demonstrations.
  - **Slide 11**: **Visual 3-Card Evolution Board**:
    - 🔴 **Phase 1: Before**: Initial Prototype (raw labels, static text, coordinate clutter, no routing/tickets).
    - 🟢 **Phase 2: Now (Built)**: CivicAlert Citizen Portal (department routing, real-time Gemini LLM, natural address entry, 1-click submit with official reference tickets).
    - 🔵 **Phase 3: Next (Roadmap)**: Future City-Wide Scaling (live CCTV bus feeds, mobile app, GIS heatmap).
  - **Slide 12**: Conclusion & Key Takeaways (Accuracy, Triage, Generative AI, and Civic Empowerment).

---

## 2. Experimental Results Summary

The model was evaluated on an independent test partition of 599 unseen infrastructure images.

### Classification Report (Independent Test Set)

```text
              precision    recall  f1-score   support

     garbage       1.00      0.99      1.00       150
      normal       0.99      0.98      0.99       150
     pothole       0.99      1.00      0.99       149
  road_crack       0.99      1.00      1.00       150

    accuracy                           0.99       599
   macro avg       0.99      0.99      0.99       599
weighted avg       0.99      0.99      0.99       599
```

### Key Performance Indicators (KPIs)

- **Test Loss**: `0.0415`
- **Reported Benchmark Test Accuracy**: `98.33%`
- **Validation Accuracy**: `99.00%` (Peak validation checkpoint)
- **Training Accuracy**: `94.59%` (Single epoch with class weights & data augmentation)
- **Inference Latency**: ~35ms per image on modern CPU architectures.
