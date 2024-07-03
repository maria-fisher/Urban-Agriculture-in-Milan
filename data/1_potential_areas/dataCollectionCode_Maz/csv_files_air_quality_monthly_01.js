// Calculate NO2 concentration (in mol/m² or μg/m²) for any study area  using Time series chart Analysis (Dataset: Sentinel-5P NRTI NO2)


var startDate = '2023-01-01';
var endDate = '2024-01-01';
var boundary = ee.FeatureCollection(roi)


// // 1. Import countries boundaries 
// // var countries = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017');


// // 2. Import Sentinel 5P NRTI NO2
// var collection = ee.ImageCollection('COPERNICUS/S5P/NRTI/L3_NO2')
//   .select('NO2_column_number_density')
//   .filterDate(startDate, endDate);


// // 3. Set visualization parameters
// var band_viz = {
//   min: 0,
//   max: 0.0002,
//   palette: ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']
// };


// // 4. Display & visualize the layer
// Map.addLayer(collection.mean().clip(roi), band_viz, 'S5P N02');
// Map.addLayer(boundary, {color: '000000', opacity: 0.5}, 'Region Boundary');
// Map.centerObject(roi, 10)


// 5. Import sentinel-5P NRTI NO2
var NO2_collection = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2')
.filterBounds(roi)
.filterDate(startDate, endDate)
.select('NO2_column_number_density')
.map(function(a){
  return a.set('month', ee.Image(a).date().get('month'))
})
print('NO2_collection', NO2_collection)

// 6. Calculate the mean NO2 concentration for each month 
var months = ee.List(NO2_collection.aggregate_array('month')).distinct()
print('Months:', months)

var NO2_monthly_conc = months.map(function(x){
  return NO2_collection.filterMetadata('month', 'equals', x).mean().set('month', x)
})
var NO2_final = ee.ImageCollection.fromImages(NO2_monthly_conc)


// 7. Create a time series chart
var chart = ui.Chart.image.series(NO2_final, roi, ee.Reducer.mean(), 1113.2,'month')
.setOptions({
title: 'NO2 Concentration',
vAxis: {title: 'Concentration(mol/m²)'},
hAxis: {title: 'Month'}
})
print('Chart', chart)