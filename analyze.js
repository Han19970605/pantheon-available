#!/usr/bin/env node
const { openSync, closeSync, writeFileSync } = require('fs');
const { join } = require('path');

const rates = ['12mbps', '24mbps', '50mbps', '100mbps', '300mbps', 'volatile'];
const losses = [0.0, 0.05, 0.2];
const delays = [0, 25];
const flows = [1, 3, 5];

const fd = openSync(join(__dirname, 'report.html'), 'w');

writeFileSync(fd, `
<!DOCTYPE html>

<head>
    <meta charset="UTF-8">
    <style>
        table {
            border-collapse: collapse;
            margin-bottom: 0.7em;
        }

        table>thead>tr:last-child {
            border-bottom: 2px solid;
        }

        th {
            font-weight: normal;
        }

        th,
        td {
            text-align: center;
            padding: 5px 10px;
        }

        .top-border {
            border-top: 1px solid;
        }

        .right-border {
            border-right: 1px solid;
        }

        .align-right {
            text-align: right;
        }

        .nowrap {
            white-space: nowrap;
        }
    </style>
</head>

<body>
    <table>
            <thead>
            <tr>
                <th rowspan="2"></th>
                <th rowspan="2" class="right-border"></th>`);

for (let rate of rates) {
    writeFileSync(fd, `<th class="right-border" colspan="${flows.length}">${rate}</th>`);
}
writeFileSync(fd, `</tr><tr>`);
for (let _ of rates) {
    for (let flow of flows) {
        writeFileSync(fd, `<th ${flow == flows[flows.length - 1] ? 'class="right-border"' : ''}>flow ${flow}</th>`);
    }
}
writeFileSync(fd, `</tr></thead><tbody>`);

for (let loss of losses) {
    for (let delay of delays) {
        writeFileSync(fd, `<tr class="top-border">`);
        writeFileSync(fd, `<td class="nowrap" rowspan="3">loss ${loss * 100}%<br>delay ${delay}ms</td>`);
        let first = true;
        for (const { key, desc, percent } of [
            { key: 'tput', desc: 'Throughput (Mbitps)' },
            { key: 'delay', desc: 'Latency (ms)' },
            { key: 'loss', desc: ' Loss (%)', percent: true },
        ]) {
            if (!first) {
                writeFileSync(fd, `</tr><tr>`);
            }
            first = false;
            writeFileSync(fd, `<td class="right-border nowrap">${desc}</td>`)
            for (let rate of rates) {
                for (let flow of flows) {
                    const name = `data-rate-${rate}-delay-${delay}-loss-${loss}-stream-${flow}`;
                    try {
                        const json = require(join(__dirname, name, 'pantheon_perf.json'));
                        // let value = json.xntp3['1'].all[key];
                        let value = json.xntp['1'].all[key];
                        if (percent) value *= 100
                        value = value.toFixed(4);
                        writeFileSync(fd, `<td class="align-right ${flow == flows[flows.length - 1] ? 'right-border' : ''}">${value}</td>`);
                    } catch (e) {
                        writeFileSync(fd, `<td ${flow == flows[flows.length - 1] ? 'class= "right-border"' : ''}>N/A</td>`);
                    }
                }
            };
        }
        writeFileSync(fd, `</tr>`);
    }
}

writeFileSync(fd, `</tbody></table></body></html>`);
closeSync(fd);
