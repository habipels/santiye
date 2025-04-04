function getChartColorsArray(a) {
    if (null !== document.getElementById(a)) {
          a = document.getElementById(a).getAttribute("data-colors");
          if (a)
                return (a = JSON.parse(a)).map(function (a) {
                      var e = a.replace(" ", "");
                      return -1 === e.indexOf(",")
                            ? getComputedStyle(document.documentElement).getPropertyValue(e) || e
                            : 2 == (a = a.split(",")).length
                            ? "rgba(" + getComputedStyle(document.documentElement).getPropertyValue(a[0]) + "," + a[1] + ")"
                            : e;
                });
    }
}
var chartHeatMapBasicColors = getChartColorsArray("basic_heatmap");
function generateData(a, e) {
    for (var t = 0, r = []; t < a; ) {
          var n = (t + 1).toString(),
                o = Math.floor(Math.random() * (e.max - e.min + 1)) + e.min;
          r.push({ x: n, y: o }), t++;
    }
    return r;
}

var options,
    chart,
    data = [
          { name: "W1", data: generateData(8, { min: 0, max: 90 }) },
          { name: "W2", data: generateData(8, { min: 0, max: 90 }) },
          { name: "W3", data: generateData(8, { min: 0, max: 90 }) },
          { name: "W4", data: generateData(8, { min: 0, max: 90 }) },
          { name: "W5", data: generateData(8, { min: 0, max: 90 }) },
          { name: "W6", data: generateData(8, { min: 0, max: 90 }) },
          { name: "W7", data: generateData(8, { min: 0, max: 90 }) },
          { name: "W8", data: generateData(8, { min: 0, max: 90 }) },
          { name: "W9", data: generateData(8, { min: 0, max: 90 }) },
          { name: "W10", data: generateData(8, { min: 0, max: 90 }) },
          { name: "W11", data: generateData(8, { min: 0, max: 90 }) },
          { name: "W12", data: generateData(8, { min: 0, max: 90 }) },
          { name: "W13", data: generateData(8, { min: 0, max: 90 }) },
          { name: "W14", data: generateData(8, { min: 0, max: 90 }) },
          { name: "W15", data: generateData(8, { min: 0, max: 90 }) },
    ],
    colors = (data.reverse(), ["#f7cc53", "#f1734f", "#663f59", "#6a6e94", "#4e88b4", "#00a7c6", "#18d8d8", "#a9d794", "#46aF78", "#a93f55", "#8c5e58", "#2176ff", "#5fd0f3", "#74788d", "#51d28c"]),
    chartHeatMapMultipleColors = (colors.reverse(), getChartColorsArray("multiple_heatmap")),
    chartHeatMapColors =
          (chartHeatMapMultipleColors &&
                ((options = {
                      series: data,
                      chart: { height: 450, type: "heatmap", toolbar: { show: !1 } },
                      dataLabels: { enabled: !1 },
                      colors: [
                            chartHeatMapMultipleColors[0],
                            chartHeatMapMultipleColors[1],
                            chartHeatMapMultipleColors[2],
                            chartHeatMapMultipleColors[3],
                            chartHeatMapMultipleColors[4],
                            chartHeatMapMultipleColors[5],
                            chartHeatMapMultipleColors[6],
                            chartHeatMapMultipleColors[7],
                      ],
                      xaxis: { type: "category", categories: ["10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "01:00", "01:30"] },
                      title: { text: "HeatMap Chart (Different color shades for each series)", style: { fontWeight: 500 } },
                      grid: { padding: { right: 20 } },
                      stroke: { colors: [chartHeatMapMultipleColors[8]] },
                }),
                (chart = new ApexCharts(document.querySelector("#multiple_heatmap"), options)).render()),
          getChartColorsArray("color_heatmap")),
    chartHeatMapShadesColors =
          (chartHeatMapColors &&
                ((options = {
                      series: [
                            { name: "Jan", data: generateData(20, { min: -30, max: 55 }) },
                            { name: "Feb", data: generateData(20, { min: -30, max: 55 }) },
                            { name: "Mar", data: generateData(20, { min: -30, max: 55 }) },
                            { name: "Apr", data: generateData(20, { min: -30, max: 55 }) },
                            { name: "May", data: generateData(20, { min: -30, max: 55 }) },
                            { name: "Jun", data: generateData(20, { min: -30, max: 55 }) },
                            { name: "Jul", data: generateData(20, { min: -30, max: 55 }) },
                            { name: "Aug", data: generateData(20, { min: -30, max: 55 }) },
                            { name: "Sep", data: generateData(20, { min: -30, max: 55 }) },
                      ],
                      chart: { height: 350, type: "heatmap", toolbar: { show: !1 } },
                      plotOptions: {
                            heatmap: {
                                  shadeIntensity: 0.5,
                                  radius: 0,
                                  useFillColorAsStroke: !0,
                                  colorScale: {
                                        ranges: [
                                              { from: -30, to: 5, name: "Low", color: chartHeatMapColors[0] },
                                              { from: 6, to: 20, name: "Medium", color: chartHeatMapColors[1] },
                                              { from: 21, to: 45, name: "High", color: chartHeatMapColors[2] },
                                              { from: 46, to: 55, name: "Extreme", color: chartHeatMapColors[3] },
                                        ],
                                  },
                            },
                      },
                      dataLabels: { enabled: !1 },
                      stroke: { width: 1 },
                      title: { text: "HeatMap Chart with Color Range", style: { fontWeight: 500 } },
                }),
                (chart = new ApexCharts(document.querySelector("#color_heatmap"), options)).render()),
          getChartColorsArray("shades_heatmap"));
chartHeatMapShadesColors &&
    ((options = {
          series: [
                { name: "birinci", data: generateData(5, { min: 0, max: 90 }) },
                { name: "İmalat Kalemi", data: generateData(3, { min: 0, max: 90 }) },
                { name: "İmalat Kalemi", data: generateData(3, { min: 0, max: 90 }) },
                { name: "İmalat Kalemi", data: generateData(3, { min: 0, max: 90 }) },
                { name: "İmalat Kalemi", data: generateData(3, { min: 0, max: 90 }) },
                { name: "İmalat Kalemi", data: generateData(3, { min: 0, max: 90 }) },
                { name: "İmalat Kalemi", data: generateData(3, { min: 0, max: 90 }) },
                { name: "İmalat Kalemi", data: generateData(3, { min: 0, max: 90 }) },
                { name: "İmalat Kalemi", data: generateData(3, { min: 0, max: 90 }) },
          ],
          chart: { height: 500, type: "heatmap", toolbar: { show: !1 } },
          stroke: { width: 0 },
          plotOptions: {
                heatmap: {
                      radius: 0,
                      enableShades: !1,
                      colorScale: {
                            ranges: [
                                  { from: 0, to: 50, color: chartHeatMapShadesColors[0] },
                                  { from: 51, to: 100, color: chartHeatMapShadesColors[1] },
                            ],
                      },
                },
          },
          dataLabels: { enabled: !0, style: { colors: ["#fff"] } },
          yaxis:{ labels: {minWidth:100, maxWidth:500, style:{ fontSize:'20px', marginRight:'50px' } }},
          xaxis: { type: "category" },
          title: { text: "Rounded (Range without Shades)", style: { fontWeight: 500 } },
    }),
    (chart = new ApexCharts(document.querySelector("#shades_heatmap"), options)).render());
