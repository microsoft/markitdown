import * as fs from 'fs';
import * as path from 'path';
import * as readline from 'readline';
import { MarkItDown, DocumentConverterResult } from './markitdown';

const markitdown = new MarkItDown();

function convertFile(filePath: string, outputFilePath?: string): void {
    const result: DocumentConverterResult = markitdown.convert(filePath);
    handleOutput(result, outputFilePath);
}

function convertStream(inputStream: NodeJS.ReadableStream, outputFilePath?: string): void {
    const result: DocumentConverterResult = markitdown.convertStream(inputStream);
    handleOutput(result, outputFilePath);
}

function handleOutput(result: DocumentConverterResult, outputFilePath?: string): void {
    if (outputFilePath) {
        fs.writeFileSync(outputFilePath, result.text_content, 'utf-8');
    } else {
        console.log(result.text_content);
    }
}

function main(): void {
    const args = process.argv.slice(2);
    const inputFilePath = args[0];
    const outputFilePath = args[1];

    if (inputFilePath) {
        convertFile(inputFilePath, outputFilePath);
    } else {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout,
            terminal: false
        });

        let inputData = '';
        rl.on('line', (line) => {
            inputData += line + '\n';
        });

        rl.on('close', () => {
            const inputStream = fs.createReadStream(inputData);
            convertStream(inputStream, outputFilePath);
        });
    }
}

main();
