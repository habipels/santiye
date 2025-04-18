{% kategori_bilgi_ver as bilgi_cagir %}
function getChartColorsArray(e) {
    if (null !== document.getElementById(e))
        return (
            (e = document.getElementById(e).getAttribute("data-colors")),
            (e = JSON.parse(e)).map(function (e) {
                var t = e.replace(" ", "");
                return -1 === t.indexOf(",")
                    ? getComputedStyle(document.documentElement).getPropertyValue(t) || t
                    : 2 == (e = e.split(",")).length
                    ? "rgba(" + getComputedStyle(document.documentElement).getPropertyValue(e[0]) + "," + e[1] + ")"
                    : t;
            })
        );
}
var upadatedonutchart,
    chartPieBasicColors = getChartColorsArray("simple_pie_chart"),
    chartDonutBasicColors =
        (chartPieBasicColors &&
            ((options = {
                series: [44, 55, 13, 43, 22],
                chart: { height: 300, type: "pie" },
                labels: ["Team A", "Team B", "Team C", "Team D", "Team E"],
                legend: { position: "right" },
                dataLabels: { dropShadow: { enabled: !1 } },
                colors: chartPieBasicColors,
            }),
            (chart = new ApexCharts(document.querySelector("#simple_pie_chart"), options)).render()),

        getChartColorsArray("simple_dount_chart")),
        chartDonutupdatingColors =
        (chartDonutBasicColors &&
            ((options = { 
                series:  {{bilgi_cagir.a}}, 
                chart: { height: 300, type: "donut" }, 
                labels: {{bilgi_cagir.b |safe}}, 
                legend: { position: "right" }, 
                dataLabels: { dropShadow: { enabled: !1 } }, 
                colors: chartDonutBasicColors
            }),
            (chart = new ApexCharts(document.querySelector("#simple_dount_chart"), options)).render()),
        getChartColorsArray("updating_donut_chart"));