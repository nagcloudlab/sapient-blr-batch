

// fs with promises
const fs = require('fs/promises'); // cjs

console.log(process.pid)

// const promise = fs.readFile('./file1.txt', 'utf-8');
// promise.then(file1Data => {
//     console.log('file1Data:\n', file1Data);
// }).catch(err => {
//     console.log('error while reading file1.txt: ', err);
// });

// console.log('do something else...');


async function readFile(filePath) {
    try {
        const fileData = await fs.readFile(filePath, 'utf-8');
        console.log(`${filePath} data:\n`, fileData);
    } catch (err) {
        console.log(`error while reading ${filePath}: `, err);
    }
}

readFile('./file1.txt');
readFile('./file2.txt');
console.log('do something else...');