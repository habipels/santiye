function getChartColorsArray(e) {
    if (null !== document.getElementById(e)) {
        var t = document.getElementById(e).getAttribute("data-colors");
        if (t)
            return (t = JSON.parse(t)).map(function (e) {
                var t = e.replace(" ", "");
                return -1 === t.indexOf(",")
                    ? getComputedStyle(document.documentElement).getPropertyValue(t) || t
                    : 2 == (e = e.split(",")).length
                    ? "rgba(" + getComputedStyle(document.documentElement).getPropertyValue(e[0]) + "," + e[1] + ")"
                    : t;
            });
        console.warn("data-colors Attribute not found on:", e);
    }
}
var worldlinemap,
    columnoptions,
    usmap,
    vectorMapWorldLineColors = getChartColorsArray("users-by-country"),
    barchartCountriesColors =
        (vectorMapWorldLineColors &&
            (worldlinemap = new jsVectorMap({
                map: "world_merc",
                selector: "#users-by-country",
                zoomOnScroll: !0,
                zoomButtons: !0,
                markers: [
                    { name: "Greenland", coords: [72, -42] },
                    { name: "Canada", coords: [56.1304, -106.3468] },
                    { name: "Brazil", coords: [-14.235, -51.9253] },
                    { name: "Egypt", coords: [26.8206, 30.8025] },
                    { name: "Russia", coords: [61, 105] },
                    { name: "China", coords: [35.8617, 104.1954] },
                    { name: "United States", coords: [37.0902, -95.7129] },
                    { name: "Norway", coords: [60.472024, 8.468946] },
                    { name: "Ukraine", coords: [48.379433, 31.16558] },
                ],
                lines: [
                    { from: "Canada", to: "Egypt" },
                    { from: "Russia", to: "Egypt" },
                    { from: "Greenland", to: "Egypt" },
                    { from: "Brazil", to: "Egypt" },
                    { from: "United States", to: "Egypt" },
                    { from: "China", to: "Egypt" },
                    { from: "Norway", to: "Egypt" },
                    { from: "Ukraine", to: "Egypt" },
                ],
                regionStyle: { initial: { stroke: "#9599ad", strokeWidth: 0.25, fill: vectorMapWorldLineColors, fillOpacity: 1 } },
                lineStyle: { animation: !0, strokeDasharray: "6 3 6" },
            })),
        getChartColorsArray("countries_charts")),
    chartAudienceColumnChartsColors =
        (barchartCountriesColors &&
            ((options = {
                series: [{ data: [1010, 1640, 490, 1255, 1050, 689, 800], name: "Sessions" }],
                chart: { type: "bar", height: 436, toolbar: { show: !1 } },
                plotOptions: { bar: { borderRadius: 4, horizontal: !0, distributed: !0, dataLabels: { position: "top" } } },
                colors: barchartCountriesColors,
                dataLabels: { enabled: !0, offsetX: 32, style: { fontSize: "12px", fontWeight: 400, colors: ["#adb5bd"] } },
                legend: { show: !1 },
                grid: { show: !1 },
                xaxis: { categories: ["R1", "R2", "R3", "R4", "R5", "R6"] },
            }),
            (chart = new ApexCharts(document.querySelector("#countries_charts2"), options)).render()),
        getChartColorsArray("audiences_metrics_charts")),
    vectorMapUsaColors =
        (chartAudienceColumnChartsColors &&
            ((columnoptions = {
                series: [
                    { name: "Last Year", data: [25.3, 12.5, 20.2, 18.5, 40.4, 25.4, 15.8, 22.3, 19.2, 25.3, 12.5, 20.2] },
                    { name: "Current Year", data: [36.2, 22.4, 38.2, 30.5, 26.4, 30.4, 20.2, 29.6, 10.9, 36.2, 22.4, 38.2] },
                ],
                chart: { type: "bar", height: 306, stacked: !0, toolbar: { show: !1 } },
                plotOptions: { bar: { horizontal: !1, columnWidth: "30%", borderRadius: 6 } },
                dataLabels: { enabled: !1 },
                legend: { show: !0, position: "bottom", horizontalAlign: "center", fontWeight: 400, fontSize: "8px", offsetX: 0, offsetY: 0, markers: { width: 9, height: 9, radius: 4 } },
                stroke: { show: !0, width: 2, colors: ["transparent"] },
                grid: { show: !1 },
                colors: chartAudienceColumnChartsColors,
                xaxis: {
                    categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                    axisTicks: { show: !1 },
                    axisBorder: { show: !0, strokeDashArray: 1, height: 1, width: "100%", offsetX: 0, offsetY: 0 },
                },
                yaxis: { show: !1 },
                fill: { opacity: 1 },
            }),
            (chart = new ApexCharts(document.querySelector("#audiences_metrics_charts"), columnoptions)).render()),
        getChartColorsArray("sales-by-locations")),
    donutchartportfolioColors =
        (vectorMapUsaColors &&
            (usmap = new jsVectorMap({ map: "us_merc_en", selector: "#sales-by-locations", regionStyle: { initial: { stroke: "#9599ad", strokeWidth: 0.25, fill: vectorMapUsaColors, fillOpacity: 1 } }, zoomOnScroll: !1, zoomButtons: !1 })),
        getChartColorsArray("portfolio_donut_charts"));
function generateData(e, t) {
    for (var o = 0, a = []; o < e; ) {
        var r = "w" + (o + 1).toString(),
            n = Math.floor(Math.random() * (t.max - t.min + 1)) + t.min;
        a.push({ x: r, y: n }), o++;
    }
    return a;
}
