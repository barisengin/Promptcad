import Ajv from "ajv";
import schema from "./schema.json";
import { DSLDocument } from "./types";

const ajv = new Ajv();
const validate = ajv.compile(schema);

export function validateDSL(dsl: unknown): { valid: boolean; errors?: string[] } {
  const valid = validate(dsl);
  if (\!valid) {
    return {
      valid: false,
      errors: validate.errors?.map((e) => `${e.instancePath} ${e.message}`) || [],
    };
  }
  return { valid: true };
}

export function isDSLDocument(obj: unknown): obj is DSLDocument {
  return validateDSL(obj).valid;
}
