---
title: icepack
theme: white
---

### Continuum mechanics and modeling

----

### Outline

* A simple problem: the heat equation
* Numerical approximation schemes
* Reynolds' transport theorem
* The Stokes equations
* Mantle convection

---

### Warm-up: the heat equation

hehe see what I did there

----

### Internal energy

* $\Omega$: some medium, a fluid or solid -- ice, rock
* $T$: the temperature of the medium.
* Non-uniform temperature $\Rightarrow$ out of thermal equilibrium.
How does the medium adjust?

----

### Internal energy

* *Internal energy density*: $E = \rho c T$.
* Temperature is *intensive*, energy is *extensive*.
* For an isolated equilibrium system,
$$\frac{\mathrm d}{\mathrm dt}\int_\Omega E\hspace{2pt}\mathrm dx = 0.$$

----

### Heat transfer

* Consider an arbitrary *control volume* $\omega$ inside $\Omega$.
* Energy inside $\omega$ changes through (1) *exchange* or *flux* across the boundary $\partial\omega$ and (2) body heating.

----

### Heat transfer

$\mathbf{F}$ = heat flux; it's a vector! $Q$ = body heating

$$\frac{\mathrm d}{\mathrm dt}\int_\omega\rho cT\hspace{2pt}\mathrm dx + \int_{\partial\omega}\mathbf{F}\cdot\mathbf{n}\hspace{2pt}\mathrm ds = \int_\omega Q\hspace{2pt}\mathrm dx$$

----

![cats](cats.png)

Red: $\mathbf F$; black: $\mathbf n$.
Things to note.
(1) $|\mathbf F|$ is larger in the illuminated patch.
(2) where does $\mathbf n$ align with $\mathbf F$?

----

### Heat flux

* But what's the heat flux?
* 2nd law $\Rightarrow$ heat flows from hot to cold.
* For simple materials, $\mathbf F = -k\nabla T$.
* If there's bulk flow at velocity $\mathbf u$,
$$\mathbf F = \rho cT\mathbf u - k\nabla T.$$

----

### PDE

* Remember the [divergence theorem](https://youtu.be/UOG3mOhv5Xo)?
$$\int_{\partial\omega}\mathbf F\cdot\mathbf n\hspace{2pt}\mathrm ds = \int_\omega\nabla\cdot\mathbf F\hspace{2pt}\mathrm dx$$
* Put all this together and you get (for all $\omega$):
$$\int_\omega\left(\frac{\partial}{\partial t}\rho cT + \nabla\cdot\mathbf F - Q\right)\mathrm dx = 0$$
* $\omega$ was arbitrary $\Rightarrow$ integrand = 0 everywhere.

----

### Recap

* The *conservation law* is the real source of truth.
* From that we can *derive* a differential equation.
* In simple geometries you can solve PDEs by hand.
* PDEs aren't fundamental -- conservation laws are!

---

### Numerical schemes

----

### Numerical methods

* Remember Fourier series? Describing a solution of the heat equation requires $\infty$ many numbers!
* All numerical schemes are just different ways to approximate with $< \infty$ numbers.

----

### Numerical methods

* Discretize a PDE $\Rightarrow$ the **finite difference method**.
* Discretize a conservation law directly $\Rightarrow$ the **finite volume method**.

----

### Variational forms

* Started with a conservation law, derived a PDE.
* There is yet a third way to express the physics: the **variational form**.
* For all *test functions* $v$,
$$\int_\Omega\left(\frac{\partial}{\partial t}\rho cT\cdot v - \mathbf F\cdot\nabla v - Qv\right)\mathrm dx = 0.$$

----

### Galerkin's method

* Discretizing the variational form gives us **Galerkin**-type methods.
* Idea: we can't describe $T$ to arbitrary resolution.
Instead, pick some *basis* functions
$$\\{\phi_1, \ldots, \phi_N\\}$$
and guess that
$$T \approx T_1(t)\phi_1(x) + \ldots + T_N(t)\phi_N(x).$$

----

### Galerkin's method

* Ok fine, now how do we pick the coefficients?
* Use the variational form, but now the test function $v$ can only come from $\\{\phi_1,\ldots,\phi_N\\}$.
* $\Rightarrow$ a finite-dimensional ODE for the coefficients!

----

### Basis functions

* Great, so how do you pick the basis?
* Fourier basis $\Rightarrow$ spectral methods
* Hat functions $\Rightarrow$ finite element method

----

Ex: spherical harmonics, a common choice of basis for global climate models.

![spherical-harmonics](https://upload.wikimedia.org/wikipedia/commons/1/12/Rotating_spherical_harmonics.gif)

----

Ex: a piecewise linear function; the FEM uses piecewise linear or polynomial functions on triangular meshes

![piecewise-linear](https://upload.wikimedia.org/wikipedia/commons/6/6d/Piecewise_linear_function2D.svg)

----

### But srsly why

|                | FDM    | FVM     | SM      | FEM
|----------------|--------|---------|---------|----
| **accuracy**   | high   | low     | high+   | high
| **shape**      | simple | complex | simple  | complex
| **jumps**      | no     | yes     | no      | sorta
| **coding**     | easy   | hard    | medium  | hard
| **adaptivity** | no     | yes     | no      | yes

----

Demonstration time!

----

### Recap

* To discretize a PDE with FDM, the inputs have to be nice.
They often aren't.
* You could also use variational forms and these lend themselves to other cool methods.

---

### Reynolds' transport theorem

----

### Extensive and intensive quantities

* Energy is *extensive* -- 2 $\times$ system size, 2 $\times$ energy
* $T$ is *intensive* -- stays the same
* Can you think of other intensive/extensive pairs?

----

### Conservation laws

* *Every* extensive quantity has a conservation law: mass, momentum, energy, chemical species, crystal orientation...
* Just a question now of what $\mathbf F$ and $q$ are.

----

### Conservation laws

$$\frac{\mathrm d}{\mathrm dt}\int_\omega \phi\hspace{2pt}\mathrm dx + \int_{\partial\omega}(\phi\mathbf u + \mathbf F)\cdot\mathbf n\mathrm ds = \int_\omega q\hspace{2pt}\mathrm dx$$

----

### The Navier-Stokes equations

* Momentum is a conserved quantity!
Take
$$\phi = \rho\mathbf u$$
in Reynolds' transport theorem.
* Real question: what is the flux?
For a perfect fluid,
$$\textbf F = p\textbf I$$
where $p$ is the hydrostatic pressure.

----

### The Navier-Stokes equations

* Denser fluids have non-trivial *shear stresses* $\boldsymbol\tau$.
* For fluids, the stress is a function of the *strain rate*
$$\boldsymbol{\dot\varepsilon} = \frac{1}{2}\left(\nabla\mathbf u + \nabla\mathbf u^\top\right).$$
* The simplest law is a *Newtonian fluid*,
$$\boldsymbol\tau = 2\mu\boldsymbol{\dot\varepsilon}$$
where $\mu$ is the *viscosity*.

----

### The Navier-Stokes equations

* Conservation law:
$$\begin{align}
& \frac{\mathrm d}{\mathrm dt}\int_\omega\rho\mathbf u\hspace{2pt}\mathrm dx + \int_{\partial\omega}(\rho\mathbf u\mathbf u^\top - \boldsymbol\tau + p\mathbf I)\cdot\mathbf n\hspace{2pt}\mathrm ds \\\\
& \qquad = \int_\omega \mathbf f\hspace{2pt}\mathrm dx
\end{align}$$
* Constitutive relation: $\boldsymbol\tau = 2\mu\boldsymbol{\dot\varepsilon}$, for example.

----

### Ice flow

* If the fluid is incompressible, then $\nabla\cdot\mathbf u = 0$.
* For ice flow, the inertial parts are tiny -- just internal stress balancing gravity.
* And ice has that weird constitutive law!

---

### Mantle convection

----

### Mantle convection

* With just the **heat** and **Stokes** equations, we can simulate flow in earth's mantle!
* **The crucial part**: warm fluid rises, cold fluid sinks.
$$\mathbf f \propto -T\cdot\mathbf g$$
* The mantle is heated from below and cooled from above, so we'll get cool convection effects!

----

Demo time...

----

### More fun

We can add more interesting effects too!
* Strain heating:
$$q = \boldsymbol\tau\cdot\boldsymbol{\dot\varepsilon}$$
* Temperature-dependent viscosity:
$$\mu \propto \exp(-T / \Delta T)$$
