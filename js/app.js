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

// Main async function that handles the OpenAI API interaction
async function main() {
    // Makes an API call to OpenAI's chat completions endpoint
    // This creates a new chat completion request
    const completion = await openai.chat.completions.create({
        // Sets up the conversation with a system message
        // Asking the AI to provide today's date
        messages: [{ role: "system", content: "Date of today" }],
        // Uses the model specified in the .env file
        // This allows for flexible model selection without changing code
        model: process.env.OPENAI_MODEL,
    });
  
    // Outputs the first response from the AI
    // choices[0] contains the primary response from the model
    console.log(completion.choices[0]);
  }

  // Immediately invokes the main function when the script runs
  main();