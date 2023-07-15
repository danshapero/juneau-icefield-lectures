import os
import numpy as np
import matplotlib.pyplot as plt
import tqdm
import firedrake
from firedrake import inner, Constant, div, dx, ds, exp
import icepack, icepack.models, icepack.solvers
from icepack.constants import (
    ice_density as ρ_I,
    water_density as ρ_W,
    weertman_sliding_law as m,
    gravity as g,
)

Lx = 50e3
nx = 50
mesh = firedrake.IntervalMesh(nx, Lx)

Q = firedrake.FunctionSpace(mesh, "CG", 2)
V = firedrake.FunctionSpace(mesh, "CG", 2)

x, = firedrake.SpatialCoordinate(mesh)

b_in, b_out = Constant(200), Constant(-400)
δb = Constant(150)
λ = Constant(0.85)
α = Constant(100.0)
expr = b_in - (b_in - b_out) * x / Lx + δb * exp(-α * (x / Lx - λ)**2)
b = firedrake.interpolate(expr, Q)

s_in, s_out = Constant(850), Constant(50)
s0 = firedrake.interpolate(s_in - (s_in - s_out) * x / Lx, Q)

h0 = firedrake.interpolate(s0 - b, Q)

h_in = s_in - b_in
δs_δx = (s_out - s_in) / Lx
τ_D = -Constant(ρ_I * g * h_in * δs_δx)

u_in, u_out = Constant(20), Constant(2400)
velocity_x = u_in + (u_out - u_in) * (x/Lx)**2
u0 = firedrake.interpolate(velocity_x, V)

T = Constant(255.0)
A = icepack.rate_factor(T)

C_0, δC = Constant(0.95), Constant(0.05)
C = firedrake.interpolate((C_0 - δC * x/Lx) * τ_D / u_in ** (1 / m), Q)

p_W = ρ_W * g * firedrake.max_value(0, h0 - s0)
p_I = ρ_I * g * h0
ϕ = 1 - p_W / p_I

def weertman_friction_with_ramp(**kwargs):
    names = ("velocity", "thickness", "surface", "friction")
    u, h, s, C = map(kwargs.__getitem__, names)
    p_W = ρ_W * g * firedrake.max_value(0, h - s)
    p_I = ρ_I * g * h
    ϕ = 1 - p_W / p_I
    return icepack.models.friction.bed_friction(velocity=u, friction=C * ϕ)

model = icepack.models.IceStream(friction=weertman_friction_with_ramp)
opts = {
    "dirichlet_ids": [1],
    "diagnostic_solver_type": "petsc",
    "diagnostic_solver_parameters": {"snes_type": "newtontr"},
}
solver = icepack.solvers.FlowSolver(model, **opts)
u0 = solver.diagnostic_solve(
    velocity=u0, thickness=h0, surface=s0, fluidity=A, friction=C
)

num_years = 250
timesteps_per_year = 2

δt = 1.0 / timesteps_per_year
num_timesteps = num_years * timesteps_per_year

a_0, δa = Constant(1.2), Constant(2.7)
a = firedrake.interpolate(a_0 - δa * x / Lx, Q)

h = h0.copy(deepcopy=True)
s = s0.copy(deepcopy=True)
u = u0.copy(deepcopy=True)

for step in tqdm.trange(num_timesteps + 1):
    h = solver.prognostic_solve(
        δt, thickness=h, accumulation=a, velocity=u, thickness_inflow=h0
    )
    s = icepack.compute_surface(thickness=h, bed=b)
    u = solver.diagnostic_solve(
        velocity=u, thickness=h, surface=s, fluidity=A, friction=C
    )

h_steady_state = h.copy(deepcopy=True)
s_steady_state = s.copy(deepcopy=True)
z_b_steady_state = firedrake.interpolate(s - h, Q)

h_min = Constant(1.0)
a_0.assign(1.05)
a.interpolate(a_0 - δa * x / Lx)
for step in tqdm.trange(2 * num_timesteps + 1):
    h = solver.prognostic_solve(
        δt, thickness=h, accumulation=a, velocity=u, thickness_inflow=h0
    )
    h = firedrake.interpolate(firedrake.max_value(h_min, h), Q)
    s = icepack.compute_surface(h=h, b=b)
    u = solver.diagnostic_solve(
        velocity=u, thickness=h, surface=s, fluidity=A, friction=C
    )

z_b = firedrake.interpolate(s - h, Q)
fig, axes = plt.subplots(figsize=(8.4, 3.2), nrows=1, ncols=2, sharex=True, sharey=True)
firedrake.plot(s_steady_state, axes=axes[0], color="tab:blue")
firedrake.plot(z_b_steady_state, axes=axes[0], color="tab:blue")
firedrake.plot(b, axes=axes[0], color="tab:brown")
firedrake.plot(s, axes=axes[1], color="tab:blue")
firedrake.plot(z_b, axes=axes[1], color="tab:blue")
firedrake.plot(b, axes=axes[1], color="tab:brown")
plt.show()
