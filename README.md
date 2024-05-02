# The N-Body Problem
 
This repository contains Python code which will simulate a number of objects interacting via gravity as described by Newton's law of gravitation.

## Background
Newton's law of gravitation states that,

$$F_i = -Gm_i \sum_{j=0}^N \frac{m_j}{|r_{ij}|^3}r_{ij},$$

where $F_i$ is the net force on object $i$, $G$ is the gravitational constant, $m$ is the mass of the subscripted object, $N$ is the total number of objects in the system and $r_{ij}$ is the displacement vector from object $i$ to object $j$.
When combined with Newton's 2nd law, $F=ma$, we can write a 2nd-order differential equation for the position of an object,

$$\frac{d^2r_i}{dt^2} = -G\sum^N_{j=0}\frac{m_j}{|r_{ij}|^3}r_{ij},$$

where $r_i$ is the position vector of object $i$. This can then be written as a system of 1st order differential equations in the form,

$\frac{du}{dt} = f(u, t)$,

where, 
```math
u = \begin{bmatrix}v\\r\end{bmatrix},
```
and, 
```math
f(u, t) = \begin{bmatrix}-G \sum\limits_{j=0}^N \frac{m_j}{|\mathrm{r}_{ij}|^3}\mathrm{r}_{ij}\\v\end{bmatrix}.
```
This system of equations is then solved by one of two integration methods.

**Forward Euler:**

$u_{k+1} = u_k + f(u_k)\Delta t$

**Leapfrog:**

$v_{i+1/2}=v_i+a_i\frac{\Delta t}{2}$\
$r_{i+1}=r_i+v_{i+1/2}\Delta t$\
$v_{i+1}=v_{i+1/2}+a_{i+1}\frac{\Delta t}{2}$

## Running a simulation
The initial conditions for the simulation should be specified as a series of `Body` class instances in a Python script named `initial_conditions.py` within a named directory (see the `sol` directory included in the repo for an example). 
The simulation can then be run using the following command structure:\
`python src/the_n_body_problem/solve_system.py <path/to/directory> -t <total time to solve for> -dt <time step> -m <integration method>`

The final orbits will be plotted in a window and the data saved to the `outputs` subdirectory.

An animation of the simulation can then be rendered using the following command structure:\
`python src/the_n_body_problem/render_animation.py <path/to/output/file> -f <fps> -d <dpi>`
 
