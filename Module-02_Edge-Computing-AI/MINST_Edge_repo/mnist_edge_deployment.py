#!/usr/bin/env python3
"""
Monica Joya
ITAI 3377: Artificial Intelligence for Edge and IoT Devices
L03: Deploying a Simple AI Model on a Simulated Edge Device
February 7, 2026

This script demonstrates the complete workflow of training a simple Convolutional Neural Network (CNN) on the MNIST dataset, converting it to TensorFlow Lite format for edge deployment, and evaluating its performance on a simulated edge device. 
"""

# ============================================================================
# STEP 1: Set Up the Environment (Load Libraries and Dependencies)
# ============================================================================
import time
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# type: ignore

print("=" * 80)
print("ITAI 3377 - MNIST Edge AI Deployment")
print("=" * 80)
print()
print("STEP 1: Loading Libraries and Dependencies")
print("-" * 80)
print(f"TensorFlow version: {tf.__version__}")
print(f"NumPy version: {np.__version__}")
print("Libraries loaded: tensorflow, keras, numpy, time, os")
print()

# ============================================================================
# STEP 2: Prepare the Dataset
# ============================================================================
print("STEP 2: Loading and Preprocessing MNIST Dataset")
print("-" * 80)

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

print(f"Original training set shape: {x_train.shape}")
print(f"Original test set shape: {x_test.shape}")

# Normalize pixel values to 0-1 range
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# Reshape to 28x28x1 (add channel dimension for CNN)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

print(f"Preprocessed training set shape: {x_train.shape}")
print(f"Preprocessed test set shape: {x_test.shape}")
print(f"Training samples: {len(x_train)}, Test samples: {len(x_test)}")
print(f"Pixel value range: [{x_train.min()}, {x_train.max()}]")
print()

# ============================================================================
# STEP 3: Train a Simple AI Model
# ============================================================================
print("STEP 3: Building and Training CNN Model")
print("-" * 80)

# Build CNN model with specified architecture
model = keras.Sequential([
    layers.Input(shape=(28, 28, 1)),
    layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dense(10, activation="softmax")
], name="MNIST_CNN")

# Display model architecture
model.summary()
print()

# Compile model
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("Model compiled successfully!")
print("Optimizer: Adam")
print("Loss: Sparse Categorical Crossentropy")
print("Metrics: Accuracy")
print()

# Train model for 5 epochs
print("Training model for 5 epochs...")
print("-" * 80)

training_start_time = time.time()
history = model.fit(
    x_train,
    y_train,
    batch_size=128,
    epochs=5,
    validation_data=(x_test, y_test),
    verbose=1
)
training_end_time = time.time()
training_duration = training_end_time - training_start_time

print()
print(f"Training completed in {training_duration:.2f} seconds")
print()

# ============================================================================
# STEP 4: Convert and Deploy the Model
# ============================================================================
print("STEP 4: Convert and Deploy the Model")
print("-" * 80)

# Save the full Keras model
keras_model_path = "mnist_model.h5"
model.save(keras_model_path)
keras_model_size = os.path.getsize(keras_model_path)
print(f"Keras model saved: {keras_model_path}")
print(f"Keras model size: {keras_model_size:,} bytes ({keras_model_size / 1024:.2f} KB)")
print()

# Convert to TFLite format
print("Converting to TFLite format...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save TFLite model
tflite_model_path = "model.tflite"
with open(tflite_model_path, "wb") as f:
    f.write(tflite_model)

tflite_model_size = os.path.getsize(tflite_model_path)
print(f"TFLite model saved: {tflite_model_path}")
print(f"TFLite model size: {tflite_model_size:,} bytes ({tflite_model_size / 1024:.2f} KB)")
print()

# Calculate size reduction
size_reduction = ((keras_model_size - tflite_model_size) / keras_model_size) * 100
print(f"Size reduction: {size_reduction:.2f}%")
print()