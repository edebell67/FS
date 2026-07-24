// Interactive CLI to create (or reset) an admin user. Deliberately prompts
// rather than accepting CLI args — args land in shell history, this
// shouldn't. Run with: npm run auth:create-admin [-- --reset]

import { createInterface } from "node:readline";
import { stdin, stdout } from "node:process";
import { eq } from "drizzle-orm";
import { config } from "dotenv";
config({ path: ".env.local" });
config();

import { db } from "../lib/db/client";
import { users } from "../lib/db/schema";
import { hashPassword } from "../lib/auth/password";

const MIN_PASSWORD_LENGTH = 12;
const ROLES = ["super_admin", "admin", "sales", "operations", "support", "read_only"] as const;

const CTRL_C = String.fromCharCode(3);
const BACKSPACE = String.fromCharCode(127);

/**
 * Wraps readline's classic event-based 'line' API in a FIFO queue instead
 * of calling rl.question() repeatedly. This matters specifically for piped
 * (non-TTY) input: readline emits 'line' for every complete line in a chunk
 * as soon as that chunk arrives, regardless of whether anything is
 * listening yet. With piped input the whole multi-line answer typically
 * arrives as a single chunk, so sequential `await rl.question()` calls miss
 * every line after the first — the 'line' events already fired before the
 * second question() attached its listener. Queueing resolvers up front and
 * handing out lines in order is correct for both TTY and piped input.
 */
function makeLineReader(rl: ReturnType<typeof createInterface>) {
  const pendingResolvers: Array<(line: string) => void> = [];
  const bufferedLines: string[] = [];

  rl.on("line", (line) => {
    const resolve = pendingResolvers.shift();
    if (resolve) resolve(line);
    else bufferedLines.push(line);
  });

  return function nextLine(): Promise<string> {
    const buffered = bufferedLines.shift();
    if (buffered !== undefined) return Promise.resolve(buffered);
    return new Promise((resolve) => pendingResolvers.push(resolve));
  };
}

/**
 * Reads a line with each keystroke echoed as '*' instead of the real
 * character. Falls back to the shared line-queue reader (unmasked) when
 * stdin isn't a real TTY (piped input, CI, etc.) — raw mode requires an
 * actual terminal.
 */
function readMaskedLine(
  prompt: string,
  nextLine: () => Promise<string>
): Promise<string> {
  if (!stdin.isTTY) {
    stdout.write(`${prompt}(no TTY detected, input will be visible) `);
    return nextLine();
  }

  return new Promise((resolve) => {
    stdout.write(prompt);
    let value = "";

    const onData = (chunk: Buffer) => {
      const str = chunk.toString("utf8");
      for (const char of str) {
        if (char === "\n" || char === "\r") {
          stdin.setRawMode?.(false);
          stdin.pause();
          stdin.removeListener("data", onData);
          stdout.write("\n");
          resolve(value);
          return;
        }
        if (char === CTRL_C) {
          stdout.write("\n");
          process.exit(1);
        }
        if (char === BACKSPACE || char === "\b") {
          if (value.length > 0) {
            value = value.slice(0, -1);
            stdout.write("\b \b");
          }
          continue;
        }
        value += char;
        stdout.write("*");
      }
    };

    stdin.resume();
    stdin.setRawMode?.(true);
    stdin.on("data", onData);
  });
}

async function main() {
  const reset = process.argv.includes("--reset");
  const rl = createInterface({ input: stdin, output: stdout });
  const nextLine = makeLineReader(rl);

  let email: string;
  let password: string;
  let role: string;
  try {
    stdout.write("Admin email: ");
    email = (await nextLine()).trim().toLowerCase();
    password = await readMaskedLine("Password (min 12 characters): ", nextLine);
    const confirmPassword = await readMaskedLine("Confirm password: ", nextLine);
    if (password !== confirmPassword) {
      console.error("Passwords did not match.");
      process.exit(1);
    }
    stdout.write(`Role [${ROLES.join(" | ")}] (default: admin): `);
    const roleInput = (await nextLine()).trim();
    role = roleInput || "admin";
  } finally {
    rl.close();
  }

  if (!email || !email.includes("@")) {
    console.error("A valid email is required.");
    process.exit(1);
  }
  if (password.length < MIN_PASSWORD_LENGTH) {
    console.error(`Password must be at least ${MIN_PASSWORD_LENGTH} characters.`);
    process.exit(1);
  }
  if (!ROLES.includes(role as (typeof ROLES)[number])) {
    console.error(`Unknown role "${role}". Must be one of: ${ROLES.join(", ")}`);
    process.exit(1);
  }

  const [existing] = await db.select().from(users).where(eq(users.email, email)).limit(1);
  if (existing && !reset) {
    console.error(
      `A user with email "${email}" already exists. Re-run with --reset to change their password.`
    );
    process.exit(1);
  }

  const passwordHash = await hashPassword(password);

  if (existing) {
    await db.update(users).set({ passwordHash, role }).where(eq(users.id, existing.id));
    console.log(`Password reset for ${email} (role: ${role}).`);
  } else {
    await db.insert(users).values({ email, passwordHash, role });
    console.log(`Created admin user ${email} (role: ${role}).`);
  }

  process.exit(0);
}

main().catch((err) => {
  console.error("Failed to create admin user:", err);
  process.exit(1);
});
