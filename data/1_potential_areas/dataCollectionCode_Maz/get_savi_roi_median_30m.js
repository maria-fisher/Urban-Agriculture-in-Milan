var startDate = '2023-01-01';
var endDate = '2024-01-01';
var boundary = ee.FeatureCollection(roi);
var L = 0.5


var dataset = ee.ImageCollection('LANDSAT/LC09/C02/T1_TOA')
  .filterDate(startDate, endDate).filterBounds(roi);
  
var calSAVI = function(image){
  var savi = image.expression(
    '((NIR - RED) / (NIR + RED + L)) * (1 + L)', {
      'NIR': image.select('B5'),
      'RED': image.select('B4'),
      'L': 0.5 //Soil Brightness Adjustment Factor
    }
).rename('SAVI').copyProperties(image, ['system:time_start']);
return savi;
};
var savicollection = dataset.map(calSAVI);
var saviclip = savicollection.map(function(image) {
  return image.clip(roi);
});

  
var trueColor432 = dataset.select(['B4', 'B3', 'B2']);
var trueColor432Vis = {
  min: 0.0,
  max: 0.4,
};

var saviVis = {
  min:-1,
  max:1,
  palette: ['red', 'yellow', 'green']
}

Map.centerObject(roi, 10)
Map.addLayer(trueColor432, trueColor432Vis, 'True Color (432)');
Map.addLayer(saviclip.median(), saviVis, 'SAVI');
Map.addLayer(boundary, {color: '000000', opacity: 0.3}, 'Region Boundary');

Export.image.toDrive({
  image: saviclip.median(), 
  description: 'savi_meadian', 
  scale: 30,
  region: roi,
  crs: saviclip.median().getInfo().crs,
  maxPixels: 1e10,
  folder: 'savi_roi_median_30m'
});
