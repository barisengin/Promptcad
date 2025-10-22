export interface DSLDocument {
  version: string
  operations: Operation[]
}

export interface Operation {
  id: string
  type: string
  params?: Record<string, any>
  inputs?: string[]
}

export interface PromptResponse {
  dsl: DSLDocument
  geometry: any
}
