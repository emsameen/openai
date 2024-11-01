//import OpenAI from "openai";
import * as readline from 'node:readline';
import * as dotenv from 'dotenv';
import {openai} from "./config/openaiConfig.js"
dotenv.config();

console.log("Hello OpenAI");
// const openai = new OpenAI();

const rl = readline.createInterface({
    input: process.stdin, 
    output: process.stdout
});

// rl.question ("Enter a question: ", (question) => console.log("Result: " + question))

async function main() {
    const completion = await openai.chat.completions.create({
        messages: [{ role: "system", content: "Date of today" }],
        model: process.env.OPENAI_MODEL,
    });
  
    console.log(completion.choices[0]);
  }

  main();