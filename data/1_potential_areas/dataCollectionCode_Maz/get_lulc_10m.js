// Define the region of interest (geometry)
var geometry = table; // table == geometry of the required zone
Map.centerObject(geometry, 10);

// Define the start and end dates
var startDate = '2023-01-01';
var endDate = '2024-01-01';

// Load the Dynamic World image collection
var dw = ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')
  .filterDate(startDate, endDate)
  .filterBounds(geometry);

// Check the available bands in the collection
print('Available bands in Dynamic World collection:', dw.first().bandNames());

// Select the 'label' band for classification
var classification = dw.select('label');

// Create a Median Composite for the classification band
var dwComposite = classification.reduce(ee.Reducer.mode());

// Check the resulting composite bands
print('Bands in dwComposite:', dwComposite.bandNames());

// Visualize the classified image (median composite)
var dwVisParams = {
  min: 0,
  max: 8,  // Adjust max value based on the classification range
  // palette: ['#419BDF', '#397D49', '#88B053', '#7A87C6', '#E49635', '#DFC35A', '#C4281B', '#A59B8F', '#B39FE1']
};

Map.addLayer(dwComposite.clip(geometry), dwVisParams, 'Mode Composite');

// Export the median composite
Export.image.toDrive({
  image: dwComposite.clip(geometry),
  description: 'Mode_Composite_Export',
  folder: 'earthengine',
  fileNamePrefix: 'lulc_zone4',
  region: geometry,
  scale: 10,
  maxPixels: 1e10,
  crs: 'EPSG:4326'
});

