#!/usr/local/bin/node
const { exec } = require('child_process');
const process = require('process');
const fs = require('fs')
const path = require('path')
// const { promises: { rmdir } } = require('fs');
const { join } = require('path')

const rates = ['12mbps', '24mbps', '50mbps', '100mbps', '200mbps', 'volatile'];
const losses = [0.0, 0.05, 0.2];
const delays = [0, 25];
const flows = [1, 3, 5];

const tasks = [];
for (const delay of delays)
    for (const loss of losses)
        for (const stream of flows)
            for (const rate of rates)
                tasks.push({ rate, delay, loss, stream });

async function runTask() {
    const task = tasks.shift();
    if (!task) return;
    const { rate, delay, loss, stream } = task;
    const name = `data-rate-${rate}-delay-${delay}-loss-${loss}-stream-${stream}`;
    let fileDir1 = path.resolve(__dirname, `./${name}`)
    // fs.mkdir(fileDir1, err=>{
    //     if(err) throw err
    //     console.log('创建成功！')
    // })
    // await rmdir(name, { recursive: true, force: true });
    const cmd =
        `src/experiments/test.py local` +
        `   --schemes "xntp"` +
        `   --uplink-trace tests/${rate}.trace` +
        `   --downlink-trace tests/${rate}.trace` +
        `   -t 20` +
        `   -f ${stream}` +
        `   --data-dir ./${name}` +
        `   --extra-mm-link-args="--uplink-queue=droptail --uplink-queue-args bytes=4000000"` +
        `   --append-mm-cmds "mm-delay ${delay} mm-loss uplink ${loss}" ` +
        `&& src/analysis/analyze.py` +
        `   --data-dir ./${name}`;
    if (process.argv.some(i => i === '-v')) console.log(cmd);
    const child = exec(cmd, { cwd: __dirname });
    child.on('exit', () => {
        delete require.cache[require.resolve(join(__dirname, name, 'pantheon_perf.json'))];
        const json = require(join(__dirname, name, 'pantheon_perf.json'));
        if (typeof json.xntp['1'] === 'undefined') {
            tasks.push({ rate, delay, loss, stream });
        }
        runTask()
    });
}

for (let i = 0; i < 4; i++) {
    runTask();
}

// process.once('beforeExit', () => rmdir(__dirname + '/tmp', { recursive: true, force: true }));

