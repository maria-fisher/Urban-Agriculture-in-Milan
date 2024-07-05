var startDate = '2023-01-01';
var endDate = '2024-01-01';
var boundary = ee.FeatureCollection(roi);

// Import Sentinel-5P OFFL NO2 ImageCollection
var collection = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CH4')
    .filterBounds(roi)
    .filterDate(startDate, endDate)
    .select('CH4_column_volume_mixing_ratio_dry_air')
    .map(function(image) {
      return image.set('month', ee.Image(image).date().get('month'));
    });

// Extract distinct months from the collection
var months = ee.List(collection.aggregate_array('month')).distinct();
print('Months:', months);

// Calculate the mean NO2 concentration for each month and print values
var monthly_conc = months.map(function(month) {
  var filteredMonth = collection.filterMetadata('month', 'equals', month);
  var meanConc = filteredMonth.mean().reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: roi,
    scale: 1113.2,  // Sentinel-5P resolution
    maxPixels: 1e10
  });
  return ee.Dictionary({
    month: month,
    concentration: meanConc.get('CH4_column_volume_mixing_ratio_dry_air')
  });
});

// Print the results as a List of Dictionaries
monthly_conc.evaluate(function(result) {
  print('Monthly Concentration:', result);
});
