---
title: Smart Inbox Env
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---
# Smart Inbox Env
## Description
Simulates email triage and response.

## Tasks
- Spam detection
- Meeting scheduling
- Complaint handling

## Actions
- classify, reply, ignore

## Run

docker build -t env .
docker run -p 8000:8000 env

## Inference

python inference.py