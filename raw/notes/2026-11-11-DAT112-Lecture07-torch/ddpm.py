# SciNet's DAT112, Neural Network Programming.
# Lecture 7, 13 May 2025. Original code: Erik Spence.
# PyTorch translation: retain the lecture's T+1 schedule and indexing.

import torch


def ddpm_schedules(beta1, beta2, T):
    """Return precomputed schedules for DDPM sampling and training."""
    if not 0 < beta1 < beta2 < 1 or T < 1:
        raise ValueError('Require 0 < beta1 < beta2 < 1 and T >= 1.')
    beta_t = (beta2 - beta1) * torch.arange(T + 1, dtype=torch.float32) / T + beta1
    sqrt_beta_t = torch.sqrt(beta_t)
    alpha_t = 1 - beta_t
    log_alpha_t = torch.log(alpha_t)
    alphabar_t = torch.exp(torch.cumsum(log_alpha_t, dim=0))
    sqrtab = torch.sqrt(alphabar_t)
    oneover_sqrta = 1 / torch.sqrt(alpha_t)
    sqrtmab = torch.sqrt(1 - alphabar_t)
    mab_over_sqrtmab_inv = (1 - alpha_t) / sqrtmab
    return {
        'alpha_t': alpha_t,
        'oneover_sqrta': oneover_sqrta,
        'sqrt_beta_t': sqrt_beta_t,
        'alphabar_t': alphabar_t,
        'sqrtab': sqrtab,
        'sqrtmab': sqrtmab,
        'mab_over_sqrtmab': mab_over_sqrtmab_inv,
    }
