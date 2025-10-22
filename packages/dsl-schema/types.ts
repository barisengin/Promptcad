export type OperationType =
  | "box"
  | "cylinder"
  | "sphere"
  | "union"
  | "subtract"
  | "fillet";

export interface BoxParams {
  width: number;
  height: number;
  depth: number;
}

export interface CylinderParams {
  radius: number;
  height: number;
}

export interface SphereParams {
  radius: number;
}

export interface FilletParams {
  radius: number;
  edges?: string[];
}

export interface Operation {
  id: string;
  type: OperationType;
  params?: BoxParams | CylinderParams | SphereParams | FilletParams | Record<string, unknown>;
  inputs?: string[];
}

export interface DSLDocument {
  version: "1.0";
  operations: Operation[];
}
