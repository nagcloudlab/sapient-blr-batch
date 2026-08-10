

const fs = require('fs'); // cjs

console.log(process.pid)

// step-1:  read the file-1
console.log('reading file1.txt...');
fs.readFile('./file1.txt', 'utf-8', (err, file1Data) => {
    if (err) {
        console.log('error while reading file1.txt: ', err);
        return;
    }
    console.log('file1Data:\n', file1Data);
});

// step-2:  read the file-2
console.log('reading file2.txt...');
fs.readFile('./file2.txt', 'utf-8', (err, file2Data) => {
    if (err) {
        console.log('error while reading file2.txt: ', err);
        return;
    }
    console.log('file2Data:\n', file2Data);
});

console.log('do something else...');