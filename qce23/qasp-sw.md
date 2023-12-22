# Quantum Aircraft Sequencing Problem with Swap-policy

## Problem settings

- Minimize total delay time $t_{f} - \underline{t}_f$ for all aircraft $f \in F$ requesting to use the runway $r \in R$.
- Each aircraft should be assigned in its time window defined between ready time $\underline{t}_f$ and due time $\overline{t}_f$.
- Each aircrft pair $(f_1, f_2 \: | \: f_1, f_2 \in F, \; f_1 \neq f_2)$ must keep minimum separation $s_{f_1 f_2}$ depends on the wake turbulence category defined by the separation manner such like RECAT-1.



## Decision variables d'original

Decision variables $x \in \mathbb{N}_0^{2 \times N_f}$ of QASP-SW consist of order decisions $x^o$ and runway decisions $x^r_i$, defined as followings:
$$
\begin{eqnarray}
x^o &=& \left\{ x^o_i \: | \forall i \in I, \: x^o_i \in \mathbb{N}_0 < N_f, \forall i, j \in I \;\; i \neq j \;\; x^0_i \neq x^o_j \right\} \\

x^r &=& \left\{ x^r_i \: | \: r^o_i \in \mathbb{N}_0 < N_r \right\} \\

I &=& \left\{ i \; | \; \forall i \in \mathbb{N}_0 < N_f \right\}

\end{eqnarray}
$$
The order decision variables can not be same values. This means the solution is represented with result of permutation of initial sequence $x^o_\mathrm{init} = \left\{ 0, \; 1, \; \cdots, \; N_f \right\}$. There is no duplication.

## Swap formulation

To ensure feasibility, QUBO formulation is changed.
Let us consider pair and contained aircraft representation.
$$
\begin{eqnarray}
P = \left\{ p_k \: | \: \forall k \in \mathbb{N}_0 < N_p \right\}
\end{eqnarray}
$$


Pair ID: $k$ $\longrightarrow$ Contained aircraft: $f_{k_1}$ and $f_{k_2}$
Pair ID: $j$ $\longrightarrow$ Contained aircraft: $f_{j_1}$ and $f_{j_2}$ qui est leader de la pair $p_k$

The cost values for aircraft of pair $p_k$:

| $(x_j, \: x_k)$ |   $f_{k_1}$   |   $f_{k_2}$   |
| :-------------: | :-----------: | :-----------: |
|   $(0, \: 0)$   | $s_{j_2 k_1}$ | $s_{k_1 k_2}$ |
|   $(1, \: 0)$   | $s_{j_1 k_1}$ | $s_{k_1 k_2}$ |
|   $(0, \: 1)$   | $s_{k_2 k_1}$ | $s_{j_2 k_2}$ |
|   $(1, \: 1)$   | $s_{k_2 k_1}$ | $s_{j_1 k_2}$ |

Then loss function for pair $p_k$ is described as below:
$$
\begin{eqnarray}
L_k &=& \bar x_k s_{k_2 k_1} + x_k s_{k_1 k_2} + \bar x_j \bar x_k s_{j_2 k_1} + x_j \bar x_k s_{j_1 k_1} + \bar x_j x_k s_{j_2 k_2} + x_j x_k s_{j_1 k_2} \\
&=& X_k^\mathrm{T} S_{kk} \bar X_k + X_j^\mathrm{T} S_{jk} \bar X_k \\
&=& X_{jk}^\mathrm{T} S_{jkkk} \bar X_k
\end{eqnarray}
$$
where vectors and matrices are defined as the followings:
$$
\begin{eqnarray}
S_{jk} &=& \begin{bmatrix}
s_{j_1 k_1} & s_{j_1 k_2} \\
s_{j_2 k_1} & s_{j_2 k_2}
\end{bmatrix} \\
S_{kk} &=& \begin{bmatrix}
0 & s_{k_1 k_2} \\
s_{k_2 k_1} & 0
\end{bmatrix} \\
S_{jkkk} &=& \begin{bmatrix} S_{jk} \\ S_{kk} \end{bmatrix}\\
X_k &=& \begin{bmatrix} x_k & \bar x_k \end{bmatrix} \\
X_{jk} &=& \begin{bmatrix} X_j & \bar X_k \end{bmatrix}
\end{eqnarray}
$$
and Negation $\bar x = 1 - x$.

Therefore total cost function is:
$$
\begin{eqnarray}
L = \sum_{k=1}^{N_p - 1} L_k = \sum_{k=1}^{N_p - 1} X_k^\mathrm{T} S_{kk}\bar X_k + X_{k-1}^\mathrm{T} S_{k-1 k} \bar X_k
\end{eqnarray}
$$
