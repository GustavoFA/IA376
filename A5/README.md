# GAN — Generative Adversarial Networks on MNIST

**Course:** IA376 — Generative Models  
**Author:** Gustavo Freitas Alves  
**Year:** 2026/1

## Overview

This project implements and trains two types of Generative Adversarial Networks (GANs) to generate images of handwritten digits (0–9) using the MNIST dataset. The notebook is structured into two main parts:

1. **Vanilla GAN** — a standard GAN implementation from scratch using PyTorch.
2. **WGAN (Wasserstein GAN)** — an improved GAN variant based on the Wasserstein distance, without gradient penalty.


## Objectives

- Construct a GAN generator and discriminator from scratch.
- Define loss functions for both components.
- Train the GAN and visualize the generated images over time.
- Implement and compare a WGAN variant.


## Dataset

**MNIST** — 60,000 grayscale images of handwritten digits (0–9), each 28×28 pixels (784 dimensions when flattened).


## Part 1 — Vanilla GAN

### Architecture

**Generator:**
- Input: noise vector of dimension `z_dim` (default: 64)
- 4 hidden blocks: Linear → BatchNorm1d → ReLU
- Final block: Linear → Sigmoid
- Output: flattened image of size 784

**Discriminator:**
- Input: flattened image of size 784
- 3 hidden blocks: Linear → LeakyReLU (slope 0.2)
- Final layer: Linear → single scalar (real/fake score)
- No sigmoid at the end (included in the loss function)

### Training Setup

| Hyperparameter | Value |
|---|---|
| Loss function | BCEWithLogitsLoss |
| Epochs | 200 |
| Noise dimension (`z_dim`) | 64 |
| Batch size | 128 |
| Learning rate | 1e-5 |
| Optimizer | Adam |

### Results

The training curves show:
- Early on, the **discriminator loss is low** — it easily distinguishes real from fake images.
- Over time, the **generator improves**, causing discriminator loss to rise.
- The generator loss stabilizes near `log(4) ≈ 1.386`, consistent with expected Vanilla GAN behavior.
- Training dynamics are stable, with no major oscillations or divergence.


## Part 2 — WGAN (Wasserstein GAN)

Based on the paper [Wasserstein GAN (Arjovsky et al., 2017)](https://arxiv.org/abs/1701.07875) and a reference PyTorch implementation.  
**Note:** This implementation does **not** use gradient penalty.

### Architecture

**Generator:**
- Input: latent vector of dimension `latent_dim` (default: 64)
- 4 blocks: Linear → (optional BatchNorm1d) → LeakyReLU
- Final layer: Linear → Tanh
- Output: image reshaped to `(1, 28, 28)`

**Critic (Discriminator):**
- Input: flattened image
- 3 blocks: Linear → LeakyReLU
- Output: single scalar (Wasserstein score, no sigmoid)

### Training Setup

Multiple training runs were performed with varying hyperparameters:

| Run | Epochs | LR | n_critic | clip_value |
|---|---|---|---|---|
| Training 0 | 200 | 1e-5 | 25 | 5e-3 |
| Training 1 | 200 | 1e-5 | 5 | 5e-3 |
| Training 2 | 200 | 5e-5 | 5 | 1e-2 |

**Common settings:**
- Batch size: 128
- Latent dimension: 64
- Optimizer: RMSprop (recommended in the WGAN paper for non-stationary problems)
- Data normalized to `[-1, 1]` range (to match Tanh output)
- Fixed noise vector used for consistent visual evaluation across training

### Key Design Choices

- **Critic trained `n_critic` times per generator step** — ensures the critic is well-trained before updating the generator.
- **Weight clipping** (`clip_value`) — enforces the Lipschitz constraint required by WGAN.
- **Wasserstein distance tracked** — used as a training signal and logged for analysis.

### Saved Artifacts

Model weights (generator + critic state dicts), training losses, and Wasserstein distances are saved as `.pt` files and available for download:

[Model files on Google Drive](https://drive.google.com/drive/folders/1zrHChoUhtGJtYJQ5sMMWjQs06k3JfsGq?usp=sharing)


## Dependencies

```
torch
torchvision
numpy
pandas
matplotlib
tqdm
```


## References

- [Goodfellow et al., 2014 — Generative Adversarial Nets](https://arxiv.org/abs/1406.2661)
- [Arjovsky et al., 2017 — Wasserstein GAN](https://arxiv.org/abs/1701.07875)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [WGAN Reference Implementation](https://github.com/rohan-paul/MachineLearning-DeepLearning-Code-for-my-YouTube-Channel/tree/master/Computer_Vision/WGAN_WITHOUT_Gradient_Penalty_from_Scratch_PyTorch)