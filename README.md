### Image Understanding Module

This module focuses on analyzing visual content within documents.

Planned capabilities include:

### Image Embedding Experiments 

This module explores visual feature extraction for multimodal question answering.

Two experimental approaches were implemented:

**1. CLIP-Based Image–Text Embedding**
- Uses OpenAI CLIP (ViT-B/32) model
- Generates image embeddings
- Generates text embeddings
- Computes cosine similarity between image and text representations

File:
- `image_embedding_hugging_face.py`

**2. YOLOv8-Based Image Feature Extraction**
- Uses YOLOv8 backbone for visual feature extraction
- Applies global average pooling to obtain image embeddings
- Uses SentenceTransformer for text embeddings
- Projects image and text features into a shared embedding space
- Computes similarity scores between modalities

File:
- `image_embedding_yolo.py`

Branch:
- `Image-Embeddings`

These experiments contribute toward integrating visual understanding into the multimodal QA pipeline.

* Image feature extraction
* Visual content interpretation
* Integration with document QA pipeline

---
