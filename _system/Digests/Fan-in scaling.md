---
id: digest-fan-in-scaling
title: Fan-in scaling source and verification record
layer: auxiliary
created: 2026-11-08
updated: 2026-11-08
---

# Fan-in scaling source and verification record

Destination: [[Learning/Probability & mathematical foundations/Random variables & distributions/Why divide weights by the square root of fan-in]]. This is a new personal observation, not a migration from the old vault.

## Authorized coverage

Current conversation, identifiable by the opening user message “for this learning note, I would like to add a very short yet interesting observation.” It includes the screenshot attachment named Image #1 and the YouTube URL below. Included through the user instructions “use 1” (Variance and standard deviation as primary home) and “but also link the other 2” (Independence versus zero covariance and Convolution of independent sums). No chat/message IDs were exposed; these are observed textual locators, not invented IDs. No older session content is ingested.

The user's requested observation is preserved as the three-input example. The mathematical derivation, independence conditions, distinction between variance and distribution, and linear/ReLU qualification are assistant synthesis. The three-input example is illustrative; the screenshot actually has ten inputs.

## Sources and access

- User-linked video: https://www.youtube.com/watch?v=P6sfmUTpUmc&t=2438s (40:38). Direct retrieval failed with a cache miss. No video transcript was read or archived.
- Image #1 was visible in the conversation. Observed code: `x = torch.randn(1000, 10)`, `w = torch.randn(10, 200)`, `y = x @ w`. Printed input mean/SD: -0.0099 / 0.9861; output mean/SD: -0.0003 / 3.0996. The supplied temporary locator `D:\CODEXS~1\temp\claudian-codex-images-Cokp3b\1-image.png` no longer existed at save time. Original bytes could not be copied or hashed; no reconstructed image or broken embed was substituted. Reattachment is needed to preserve and embed the original.
- Read PyTorch's initialization reference during this conversation: https://docs.pytorch.org/docs/2.15/nn.init.html#torch.nn.init.kaiming_normal_ and the `calculate_gain` table. Checked SD = gain / sqrt(fan-in), linear gain 1, and ReLU gain sqrt(2).

## Mathematical verification

Checked analytically: independence factors E[XW] and E[X²W²]; each standard-normal product has mean zero and variance one; independence across pairs makes all cross-covariances zero; variance scales quadratically under deterministic multiplication. Thus the three-input SD is sqrt(3), and scaling weights by 1/sqrt(n) gives unconditional unit output variance for the stated zero-bias linear setup. No claim of exact Gaussian output or fixed-weight unit variance is made. The screenshot's finite-sample SD is supporting illustration, not a proof. No code from the video was executed.

Structural validation results are recorded in [[_system/Log]]. Video access remains an explicit limitation, tracked in [[_system/Review Queue]].

## Screenshot supplied in the vault and formatting repair (2026-11-08)

The user subsequently pasted [[kaiming_scaling.png]] into the learning note. Inspected the image and confirmed the same displayed code, histograms and printed moments. File size: 617720 bytes; SHA-256: `7ba9e7c61cfcdc34f6d0c7ac99640e18b2f2903f287e43f3925d0b18f36b24b0`. The missing-original-image item is resolved by this user-supplied vault copy, without claiming byte equality to the unavailable temporary attachment. Kept the file and its existing embed in place; no attachment settings, source properties or map relationships were changed. Replaced chat-style math delimiters with Obsidian inline dollar signs and display double-dollar fences. No new learning material or video transcript was ingested.
