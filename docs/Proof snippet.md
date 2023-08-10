Proof snippet

For both classical and quantum case, we use the pretty same sketch.

If we apply $X$ or $Z$ on a bit, before the process, it is equivalent to applying an operator $U$ afterward. $U$ may have some sense of locality. In the classical case, we just apply $X$.

- A CNOT from a to b, converts $X^{(a)}$ to $X^{(a)}\otimes X^{(b)}$ and $Z^{(b)}$ to $Z^{(a)}\otimes Z^{(b)}$.

- Any other $U$ which is not $X^{(a)}$ or $Z^{(b)}$ cannot be converted to those outputs by a CNOT.

- Those conversions could not be done with $CR_x(\theta)$ for $\theta \ne \pi/2$ plus local operations.

- TODO:  A fact that shows any non-prefect transition will transfer less than a bit.

Now, our problem is that if we have qubits $f, c_1\dots c_n, l$

- $X^{(f)}$ should be equivalent to applying $X^{(f)} \otimes X^{(l)}$ afterward and $Z^{(l)}$ should be equivalent to applying $Z^{(f)} \otimes Z^{(l)}$ afterward.

- $Z/X^{(c_i)}$ should remain as it is for any $i$.

Assume three adjacent qubits, $C_{i-1}, C_{i}, C_{i+1}$

- Deffering operator of $X^{(f)}$ should act (trivially, non-trivially, trivially) at different points on $C_i$.

- The similar fact is true for $C_{i+1}$.

We need 2n to carry $X$ and 2n to carry $Z$.