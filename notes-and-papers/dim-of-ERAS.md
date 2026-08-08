For one snapshot and one ensemble member:

- C3S temperature: $180 \times 360 = 64,800$ state dimensions.
- ERA5 temperature after alignment: $64,800$.
- Station-temperature observations: $1,592$ observation dimensions—irregular points, not a grid.
- C3S sea ice: $40 \times 360 = 14,400$ state dimensions.
- ERA5 sea ice: $14,400$.
- OSI SAF sea ice observations: $14,400$.

The 51 ensembles are $N = 51$ samples of the state; they are not part of $d_x$.

If temperature and sea ice are both placed on the Arctic $40 \times 360$ grid:

```math
d_x = 2 \text{ variables} \times 40 \times 360 = 28,800
```

So each ensemble member would be one $28,800$-dimensional state vector.
