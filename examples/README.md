### Run examples

*Note*: You should always start examples from root directory of pylocating.

#### Federated Particles

Two separated environments contain a different number of particles.
All the particles are `PSOParticle` (they follow a standard PSO model).
The initial position of particles are around the beacons.

```bash
/path/to/pylocating$ scripts/bestfitnessgraph.sh federated_particles 20 10
```

arguments:
  - 20: the first environment contains 20 particles
  - 10: the second environment contains 10 particles


#### FollowBest Particles

Two connected environments contain a different number of particles.
The first environment contains `GlobalBestPSOParticle` particles (the same of
`PSOParticle`, but in this case the best fitness is the best found by all
environments instead of the best found inside the environment itself).
The second environment contains `FollowBestParticle`; they are special
particles that only search around the globally found best position in that
moment.

```bash
/path/to/pylocating$ scripts/bestfitnessgraph.sh followbest_particles 20 10
```

arguments:
  - 20: the first environment contains 20 particles
  - 10: the second environment contains 10 particles


#### Start from beacon sphere surface

One single environment contains all particles.
Them are equally distributed around the beacons on the sphere surface with
center the beacon itself and radius the distance measured.
3/4 of all particles are `PSOParticle`. The rest are `FollowBestParticle`.

```bash
/path/to/pylocating$ scripts/bestfitnessgraph.sh start_from_sphere_surface 16
```

arguments:
  - 16: the environment contains 16 particles.

*note*: the number of particle should be divisible for 4 (the number of
 beacons).
