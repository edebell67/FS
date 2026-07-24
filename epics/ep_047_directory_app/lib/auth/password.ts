import { randomBytes, scrypt as scryptCallback, timingSafeEqual } from "node:crypto";
import { promisify } from "node:util";

const scrypt = promisify(scryptCallback);
const KEY_LENGTH = 64;
const ENCODING = "scrypt";

/**
 * Produces a salted, memory-hard password hash suitable for persisted admin
 * accounts. Plaintext passwords are never stored.
 */
export async function hashPassword(password: string): Promise<string> {
  if (!password) throw new Error("Password must not be empty");

  const salt = randomBytes(16).toString("base64url");
  const derived = (await scrypt(password, salt, KEY_LENGTH)) as Buffer;
  return `${ENCODING}$${salt}$${derived.toString("base64url")}`;
}

/** Returns true only if the supplied password matches a hash from hashPassword. */
export async function verifyPassword(password: string, encodedHash: string): Promise<boolean> {
  const [algorithm, salt, expected] = encodedHash.split("$");
  if (algorithm !== ENCODING || !salt || !expected) return false;

  const derived = (await scrypt(password, salt, KEY_LENGTH)) as Buffer;
  const expectedBuffer = Buffer.from(expected, "base64url");
  return expectedBuffer.length === derived.length && timingSafeEqual(expectedBuffer, derived);
}
