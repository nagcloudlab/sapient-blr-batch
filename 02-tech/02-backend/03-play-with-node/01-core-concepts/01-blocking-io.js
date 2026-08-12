

const fs = require('fs'); // cjs

console.log(process.pid)

// step-1:  read the file-1
const file1Data = fs.readFileSync('./file1.txt', 'utf-8'); // blocking call
console.log('file1Data: \n', file1Data);

// step-2:  read the file-2
const file2Data = fs.readFileSync('./file2.txt', 'utf-8'); // blocking call
console.log('file2Data: \n', file2Data);

console.log('do something else...');