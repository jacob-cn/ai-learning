import { GoogleGenerativeAI } from "@google/generative-ai";
import * as dotenv from "dotenv";
import * as readline from "readline";

dotenv.config();

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);

// This is the key to structured output — tell the model exactly what JSON to return
const SYSTEM_PROMPT = `You are an expert Android/Kotlin code reviewer with 10+ years experience.
When given code, analyze it and respond ONLY with a valid JSON object in this exact structure:

{
  "summary": "Brief overall assessment",
  "score": <number 1-10>,
  "issues": [
    {
      "severity": "critical" | "warning" | "suggestion",
      "category": "performance" | "security" | "best_practice" | "readability" | "architecture",
      "line": "<line number or range if known, else null>",
      "issue": "What the problem is",
      "fix": "How to fix it with example code if possible"
    }
  ],
  "positives": ["thing done well", "another good thing"],
  "verdict": "approve" | "approve_with_changes" | "request_changes"
}

Return ONLY the JSON. No markdown, no explanation, no backticks.`;

// Define TypeScript types matching our JSON structure
interface CodeIssue {
  severity: "critical" | "warning" | "suggestion";
  category: "performance" | "security" | "best_practice" | "readability" | "architecture";
  line: string | null;
  issue: string;
  fix: string;
}

interface ReviewResult {
  summary: string;
  score: number;
  issues: CodeIssue[];
  positives: string[];
  verdict: "approve" | "approve_with_changes" | "request_changes";
}

async function reviewCode(code: string): Promise<ReviewResult> {
  const model = genAI.getGenerativeModel({
    model: "gemini-2.5-flash",
    systemInstruction: SYSTEM_PROMPT,
  });

  const result = await model.generateContent(code);
  const text = result.response.text();

  // Parse the JSON response
  const cleaned = text.replace(/```json|```/g, "").trim();
  return JSON.parse(cleaned) as ReviewResult;
}

// Pretty print the review in terminal
function printReview(review: ReviewResult): void {
  console.log("\n" + "=".repeat(60));
  console.log(`📊 SCORE: ${review.score}/10`);
  console.log(`📝 SUMMARY: ${review.summary}`);
  console.log(`🏁 VERDICT: ${review.verdict.toUpperCase().replace("_", " ")}`);

  if (review.positives.length > 0) {
    console.log("\n✅ POSITIVES:");
    review.positives.forEach(p => console.log(`  • ${p}`));
  }

  if (review.issues.length > 0) {
    console.log("\n🔍 ISSUES:");
    review.issues.forEach(issue => {
      const icon = issue.severity === "critical" ? "🔴" 
                 : issue.severity === "warning"  ? "🟡" 
                 : "🔵";
      console.log(`\n  ${icon} [${issue.severity.toUpperCase()}] ${issue.category}`);
      if (issue.line) console.log(`     Line: ${issue.line}`);
      console.log(`     Issue: ${issue.issue}`);
      console.log(`     Fix: ${issue.fix}`);
    });
  }

  console.log("\n" + "=".repeat(60) + "\n");
}

async function main() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  console.log("🤖 Android Code Reviewer");
  console.log("Paste your Kotlin/Android code, then type END on a new line.\n");

  const askForCode = () => {
    const lines: string[] = [];

    const collectLines = (line: string) => {
      if (line.trim() === "END") {
        rl.removeListener("line", collectLines);

        const code = lines.join("\n");
        if (!code.trim()) {
          console.log("No code entered.\n");
          askForCode();
          return;
        }

        console.log("\n⏳ Reviewing your code...\n");

        reviewCode(code)
          .then(review => {
            printReview(review);
            rl.question("Review another? (y/n): ", answer => {
              if (answer.toLowerCase() === "y") {
                console.log("\nPaste your next code snippet, then type END:\n");
                askForCode();
              } else {
                console.log("Goodbye!");
                rl.close();
              }
            });
          })
          .catch(err => {
            console.error("Error reviewing code:", err.message);
            askForCode();
          });
      } else {
        lines.push(line);
      }
    };

    rl.on("line", collectLines);
  };

  askForCode();
}

main();
