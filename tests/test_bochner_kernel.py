"""
Unit Tests for Bochner Harmonic Continuous Fourier Temporal Embedding
=====================================================================
Validates Bochner's Theorem properties:
- Dimension guarantees across diverse batch sizes and embedding dimensions
- Periodicity under individual angular frequencies
- Continuous temporal translation invariance: <Phi(t1 + c), Phi(t2 + c)> == <Phi(t1), Phi(t2)>
- Smooth Lipschitz continuity across infinitesimal delta t
- Gradient flow into Fourier frequencies and scale parameters
"""

import math
import pytest
import torch
import numpy as np

from synapselex.src.models.tgat_core import HarmonicTimeEmbedding, DualClockHarmonicEmbedding


class TestBochnerHarmonicKernel:
    
    @pytest.mark.parametrize("d_time", [8, 16, 32, 64])
    def test_output_dimensions(self, d_time):
        """Embedding dimension must strictly equal d_time for 1D and 2D inputs."""
        layer = HarmonicTimeEmbedding(time_dim=d_time)
        
        # 1D input [M]
        delta_t_1d = torch.tensor([0.0, 10.5, 365.25, 1095.0, 2000.0], dtype=torch.float32)
        out_1d = layer(delta_t_1d)
        assert out_1d.shape == (5, d_time), f"Expected (5, {d_time}), got {out_1d.shape}"
        
        # 2D input [M, 1]
        delta_t_2d = delta_t_1d.unsqueeze(-1)
        out_2d = layer(delta_t_2d)
        assert out_2d.shape == (5, d_time)
        assert torch.allclose(out_1d, out_2d, atol=1e-6)

    def test_odd_dimension_raises_assertion(self):
        """Bochner sine/cosine pairs require an even embedding dimension."""
        with pytest.raises(AssertionError):
            HarmonicTimeEmbedding(time_dim=15)

    def test_periodicity_property(self):
        """
        For any constituent angular frequency omega_k, a shift by period
        T_k = 2 * pi / omega_k must reproduce the harmonic component.
        """
        layer = HarmonicTimeEmbedding(time_dim=16)
        freqs = layer.frequencies.detach().clone()
        
        t0 = torch.tensor([42.0], dtype=torch.float32)
        half_dim = layer.time_dim // 2
        
        for k in range(half_dim):
            omega_k = freqs[k].item()
            period_k = (2.0 * math.pi) / omega_k
            t_shifted = t0 + period_k
            
            emb_orig = layer(t0).detach()
            emb_shifted = layer(t_shifted).detach()
            
            # Cosine component at index k
            cos_orig = emb_orig[0, k].item()
            cos_shifted = emb_shifted[0, k].item()
            # Sine component at index half_dim + k
            sin_orig = emb_orig[0, half_dim + k].item()
            sin_shifted = emb_shifted[0, half_dim + k].item()
            
            assert pytest.approx(cos_orig, abs=1e-4) == cos_shifted, f"Cosine periodicity failed at component {k}"
            assert pytest.approx(sin_orig, abs=1e-4) == sin_shifted, f"Sine periodicity failed at component {k}"

    def test_shift_invariance_bochner_theorem(self):
        """
        Bochner Theorem Shift-Invariance:
        The stationary kernel K(t1, t2) = <Phi(t1), Phi(t2)> depends solely on the time
        difference Delta t = t1 - t2. For any temporal translation c,
        <Phi(t1 + c), Phi(t2 + c)> must equal <Phi(t1), Phi(t2)>.
        """
        layer = HarmonicTimeEmbedding(time_dim=32)
        
        t1 = torch.tensor([150.0], dtype=torch.float32)
        t2 = torch.tensor([515.0], dtype=torch.float32)
        
        phi_t1 = layer(t1)
        phi_t2 = layer(t2)
        kernel_base = torch.sum(phi_t1 * phi_t2).item()
        
        # Test across multiple arbitrary temporal shifts c
        for shift in [30.0, 180.5, 365.25, 1095.0, -100.0, 5000.0]:
            t1_shift = t1 + shift
            t2_shift = t2 + shift
            
            phi_t1_shift = layer(t1_shift)
            phi_t2_shift = layer(t2_shift)
            kernel_shifted = torch.sum(phi_t1_shift * phi_t2_shift).item()
            
            assert pytest.approx(kernel_base, abs=1e-4) == kernel_shifted, (
                f"Shift invariance violated for shift c={shift}: {kernel_base} vs {kernel_shifted}"
            )

    def test_smooth_continuity(self):
        """As epsilon -> 0, ||Phi(t + epsilon) - Phi(t)||_2 must converge to 0 smoothly."""
        layer = HarmonicTimeEmbedding(time_dim=32)
        t = torch.tensor([730.0], dtype=torch.float32)
        phi_t = layer(t)
        
        prev_dist = float("inf")
        for exp in [1.0, 0.1, 0.01, 0.001, 0.0001]:
            eps = torch.tensor([exp], dtype=torch.float32)
            phi_eps = layer(t + eps)
            dist = torch.norm(phi_eps - phi_t, p=2).item()
            assert dist < prev_dist, f"Distance should monotonically decrease with epsilon: {dist} vs {prev_dist}"
            prev_dist = dist
        
        assert prev_dist < 1e-3, "Infinitesimal shift distance did not converge to zero."

    def test_gradient_flow_and_backprop(self):
        """Validates that continuous temporal embeddings propagate non-zero gradients."""
        layer = HarmonicTimeEmbedding(time_dim=16)
        delta_t = torch.tensor([100.0, 500.0, 1200.0], dtype=torch.float32, requires_grad=True)
        
        emb = layer(delta_t)
        loss = torch.sum(emb ** 2)
        loss.backward()
        
        assert delta_t.grad is not None, "Delta_t gradient should not be None."
        assert not torch.all(delta_t.grad == 0), "Delta_t gradients should be non-vanishing."
        assert layer.frequencies.grad is not None, "Frequency gradients should not be None."
        assert layer.scale.grad is not None, "Scale gradient should not be None."

    def test_dual_clock_harmonic_embedding(self):
        """Validates Coupled Dual-Clock Deontic Embedding [Phi_{d/2}(t) || Phi_{d/2}(tau)]."""
        dual = DualClockHarmonicEmbedding(time_dim=32)
        t_phys = torch.tensor([1200.0], dtype=torch.float32)
        tau_proc = torch.tensor([500.0], dtype=torch.float32)
        
        emb = dual(t_phys, tau_proc)
        assert emb.shape == (1, 32)
        
        # When tau_proc is None, default to t_phys
        emb_default = dual(t_phys)
        assert emb_default.shape == (1, 32)
        # Slices should match when inputs are identical
        assert torch.allclose(emb_default[:, :16], emb_default[:, 16:], atol=1e-6)
