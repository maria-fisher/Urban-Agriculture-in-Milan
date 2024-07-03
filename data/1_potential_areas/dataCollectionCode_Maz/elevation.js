//DEM Data
// i have added line 5, 8, 18, 34

var startDate = '2000-02-11';
var endDate = '2000-02-22';
var boundary = ee.FeatureCollection(roi_zone_4);

var dataset_DEM = ee.Image('USGS/SRTMGL1_003');
var elevation = dataset_DEM.select('elevation').clip(roi_zone_4);

// print(dataset_DEM)

var dem_visualization = {
  bands: ['0'],
  //min: 0.0,
  //max: 2,
};

Map.centerObject(roi_zone_4, 12)
//Map.addLayer(dataset_DEM, dem_visualization, 'DEM Color (432)');
//DEM Layer
Map.addLayer(dataset_DEM, {min: 0, max: 4000, palette: ['blue', 'green', 'yellow', 'red']}, 'SRTM DEM');
//Slope
var slope = ee.Terrain.slope(dataset_DEM);
// Display the slope layer on the map
Map.addLayer(slope, {min: 0, max: 45, palette: ['blue', 'yellow', 'red']}, 'Slope')

// Compute the terrain roughness
var roughness = slope.reduceNeighborhood({
  reducer: ee.Reducer.stdDev(),
  kernel: ee.Kernel.square(3)
});

Map.addLayer(roughness, {min: 0, max: 10, palette: ['white', 'gray', 'black']}, 'Roughness');
Map.addLayer(boundary, {color: '000000', opacity: 0.3}, 'Region Boundary');
//

