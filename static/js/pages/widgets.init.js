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
            (chart = new ApexCharts(document.querySelector("#countries_charts"), options)).render()),
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
donutchartportfolioColors &&
    ((options = {
        series: [19405, 40552, 15824, 30635],
        labels: ["Bitcoin", "Ethereum", "Litecoin", "Dash"],
        chart: { type: "donut", height: 210 },
        plotOptions: {
            pie: {
                size: 100,
                offsetX: 0,
                offsetY: 0,
                donut: {
                    size: "70%",
                    labels: {
                        show: !0,
                        name: { show: !0, fontSize: "18px", offsetY: -5 },
                        value: {
                            show: !0,
                            fontSize: "20px",
                            color: "#343a40",
                            fontWeight: 500,
                            offsetY: 5,
                            formatter: function (e) {
                                return "$" + e;
                            },
                        },
                        total: {
                            show: !0,
                            fontSize: "13px",
                            label: "Total value",
                            color: "#9599ad",
                            fontWeight: 500,
                            formatter: function (e) {
                                return (
                                    "$" +
                                    e.globals.seriesTotals.reduce(function (e, t) {
                                        return e + t;
                                    }, 0)
                                );
                            },
                        },
                    },
                },
            },
        },
        dataLabels: { enabled: !1 },
        legend: { show: !1 },
        yaxis: {
            labels: {
                formatter: function (e) {
                    return "$" + e;
                },
            },
        },
        stroke: { lineCap: "round", width: 2 },
        colors: donutchartportfolioColors,
    }),
    (chart = new ApexCharts(document.querySelector("#portfolio_donut_charts"), options)).render());
var chartHeatMapColors = getChartColorsArray("color_heatmap"),
    areachartbitcoinColors =
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
                chart: { height: 310, type: "heatmap", toolbar: { show: !1 } },
                legend: { show: !1 },
                plotOptions: {
                    heatmap: {
                        shadeIntensity: 0.5,
                        radius: 0,
                        useFillColorAsStroke: !0,
                        colorScale: {
                            ranges: [
                                { from: -30, to: 5, name: "Youtube", color: chartHeatMapColors[0] },
                                { from: 6, to: 20, name: "Meta", color: chartHeatMapColors[1] },
                                { from: 21, to: 45, name: "Google", color: chartHeatMapColors[2] },
                                { from: 46, to: 55, name: "Medium", color: chartHeatMapColors[3] },
                                { from: 36, to: 40, name: "Other", color: chartHeatMapColors[4] },
                            ],
                        },
                    },
                },
                dataLabels: { enabled: !1 },
                stroke: { width: 1 },
                title: { style: { fontWeight: 500 } },
            }),
            (chart = new ApexCharts(document.querySelector("#color_heatmap"), options)).render()),
        getChartColorsArray("results_sparkline_charts"));
areachartbitcoinColors &&
    ((options = {
        series: [{ name: "Results", data: [0, 68, 35, 90, 99] }],
        chart: { width: 140, type: "area", sparkline: { enabled: !0 }, toolbar: { show: !1 } },
        dataLabels: { enabled: !1 },
        stroke: { curve: "smooth", width: 1.5 },
        fill: { type: "gradient", gradient: { shadeIntensity: 1, inverseColors: !1, opacityFrom: 0.45, opacityTo: 0.05, stops: [50, 100, 100, 100] } },
        colors: areachartbitcoinColors,
    }),
    (chart = new ApexCharts(document.querySelector("#results_sparkline_charts"), options)).render()),
    (areachartbitcoinColors = getChartColorsArray("results_sparkline_charts2")) &&
        ((options = {
            series: [{ name: "Results", data: [0, 98, 85, 90, 67] }],
            chart: { width: 140, type: "area", sparkline: { enabled: !0 }, toolbar: { show: !1 } },
            dataLabels: { enabled: !1 },
            stroke: { curve: "smooth", width: 1.5 },
            fill: { type: "gradient", gradient: { shadeIntensity: 1, inverseColors: !1, opacityFrom: 0.45, opacityTo: 0.05, stops: [50, 100, 100, 100] } },
            colors: areachartbitcoinColors,
        }),
        (chart = new ApexCharts(document.querySelector("#results_sparkline_charts2"), options)).render());
(areachartbitcoinColors = getChartColorsArray("results_sparkline_charts3")) &&
    ((options = {
        series: [{ name: "Results", data: [0, 65, 103, 75, 120] }],
        chart: { width: 140, type: "area", sparkline: { enabled: !0 }, toolbar: { show: !1 } },
        dataLabels: { enabled: !1 },
        stroke: { curve: "smooth", width: 1.5 },
        fill: { type: "gradient", gradient: { shadeIntensity: 1, inverseColors: !1, opacityFrom: 0.45, opacityTo: 0.05, stops: [50, 100, 100, 100] } },
        colors: areachartbitcoinColors,
    }),
    (chart = new ApexCharts(document.querySelector("#results_sparkline_charts3"), options)).render());
var options,
    chart,
    swiper = new Swiper(".mySwiper", { slidesPerView: "auto", spaceBetween: 30, pagination: { el: ".swiper-pagination", clickable: !0 }, autoplay: { delay: 2500, disableOnInteraction: !1 } }),
    card =
        (document.addEventListener("DOMContentLoaded", function (e) {
            var a = document.getElementById("card-num-input"),
                t = ((cardNumElem = document.getElementById("card-num-elem")), document.getElementById("card-holder-input")),
                o = document.getElementById("card-holder-elem"),
                r = document.getElementById("expiry-month-input"),
                n = document.getElementById("expiry-month-elem"),
                i = document.getElementById("expiry-year-input"),
                s = document.getElementById("expiry-year-elem"),
                l = document.getElementById("cvc-input"),
                c = document.getElementById("cvc-elem"),
                d = document.getElementById("custom-card-form");
            (a.onkeydown = function (e) {
                var t = e.keyCode || e.charCode,
                    o = (48 <= t && t <= 57) || (96 <= t && t <= 105);
                if (!o && !(8 == t || 46 == t)) return !1;
                (t = e.target.value), (e = t.length);
                !o || (4 != e && 9 != e && 14 != e) || (a.value = t + " ");
            }),
                (a.onkeyup = function (e) {
                    var t = e.keyCode || e.charCode,
                        o = (48 <= t && t <= 57) || (96 <= t && t <= 105);
                    if (!o && !(8 == t || 46 == t)) return !1;
                    var a = e.target.value,
                        r = a.length,
                        n = "XXXX XXXX XXXX XXXX".split("");
                    !o || (4 != r && 9 != r && 14 != r) || (n[r] = " ");
                    for (var i = 0; i < r; i++) n[i] = a.charAt(i);
                    cardNumElem.innerText = n.join("");
                }),
                (t.onkeyup = function (e) {
                    o.innerText = e.target.value;
                }),
                (r.onchange = function (e) {
                    e.target.value || (n.innerText = "00"), (n.innerText = e.target.value);
                }),
                (i.onchange = function (e) {
                    e.target.value || (s.innerText = "0000"), (s.innerText = e.target.value);
                }),
                (l.onkeyup = function (e) {
                    for (var t = e.target.value, o = ["_", "_", "_"], a = 0; a < t.length; a++) o[a] = t.charAt(a);
                    c.innerText = o.join("");
                }),
                (d.onsubmit = function (e) {
                    e.preventDefault();
                });
        }),
        new Card({
            form: document.querySelector("#card-form-elem"),
            container: ".card-wrapper",
            formSelectors: { numberInput: "input#card-number-input", expiryInput: "input#card-expiry-input", cvcInput: "input#card-cvc-input", nameInput: "input#card-name-input" },
            placeholders: { number: "•••• •••• •••• ••••", name: "Adı Soyadı", expiry: "••/••", cvc: "•••" },
            masks: { cardNumber: "•" },
        }));
Array.from(document.querySelectorAll("#candidate-list li")).forEach(function (a) {
    a.querySelector("a").addEventListener("click", function () {
        var e = a.querySelector(".candidate-name").innerHTML,
            t = a.querySelector(".candidate-position").innerHTML,
            o = a.querySelector(".candidate-img").src;
        (document.getElementById("candidate-name").innerHTML = e), (document.getElementById("candidate-position").innerHTML = t), (document.getElementById("candidate-img").src = o);
    });
}),
    window.addEventListener("load", () => {
        var o = document.getElementById("searchList"),
            a = document.querySelectorAll("#candidate-list li");
        o.onkeyup = () => {
            var e,
                t = o.value.toLowerCase();
            for (e of a) -1 == e.querySelector(".candidate-name").innerHTML.toLowerCase().indexOf(t) ? e.classList.add("d-none") : e.classList.remove("d-none");
        };
    }),
    document.getElementById("confirm-btn").addEventListener("click", function () {
        var e;
        document.querySelector("input[name=listGroupRadioGrid]:checked")
            ? ((document.getElementById("notification-overlay").style.visibility = "visible"),
              (document.getElementById("notification-overlay").style.opacity = "1"),
              (e = document.querySelector("input[name=listGroupRadioGrid]:checked").parentElement.querySelector(".pay-amount").innerHTML),
              (document.querySelector("#notification-overlay .success-pay").innerHTML = e))
            : (document.getElementById("notification-warn").classList.remove("d-none"), setTimeout(() => document.getElementById("notification-warn").classList.add("d-none"), 2e3));
    }),
    document.getElementById("back-btn").addEventListener("click", function () {
        (document.getElementById("notification-overlay").style.visibility = "hidden"), (document.getElementById("notification-overlay").style.opacity = "0");
    });
