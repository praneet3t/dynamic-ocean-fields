# Ocean Grid Data Format

## File Structure

The ocean grid data is stored as 3D NumPy arrays with shape `(height, width, features)`.

## Features (4 channels)

1. **Wave Height** (index 0): Normalized wave height (0-1)
   - 0 = calm water
   - 1 = maximum wave height

2. **Current Velocity** (index 1): Normalized current speed (0-1)
   - 0 = no current
   - 1 = maximum current speed

3. **Temperature** (index 2): Normalized water temperature (0-1)
   - 0 = coldest
   - 1 = warmest
   - Optimal navigation temperature ≈ 0.5

4. **Depth** (index 3): Normalized water depth (0-1)
   - 0 = shallowest (high cost)
   - 1 = deepest (low cost)

## Sample Data

`sample_grid.npy` contains a 20x20 grid with realistic environmental patterns:
- Wave heights increase near boundaries
- Temperature gradient from north to south
- Depth increases toward center
- Random current variations

## Data Sources

Real ocean data can be obtained from:
- NOAA Ocean Service
- Copernicus Marine Service
- ECMWF ERA5 reanalysis
- Satellite altimetry data

Convert real data to the normalized 4-channel format for use with this environment.