import * as v from 'valibot'
import * as core from '@actions/core'

v.setGlobalMessage(
  e =>
    `Validation Error: {type: ${e.type}, kind: ${e.kind}, received: ${e.received}, expected: ${e.expected}, message: ${e.message}}`
)

const architectureSchema = v.union(
  [
    v.literal('AMD64'),
    v.literal('ARM64'),
    v.literal('ARMv6'),
    v.literal('ARMv7'),
    v.literal('RISCV'),
    v.literal('UNKNOWN')
  ],
  e => `architecture error: ${e.message}`
)

const imageSchema = v.object({
  type: v.literal('IMAGE'),
  classification: v.union([v.literal('RFSIMAGE'), v.literal('YOCTO')])
})

const packageSchema = v.object({
  type: v.union([
    v.literal('FILE'),
    v.literal('ARCHIVE'),
    v.literal('FIRMWARE')
  ]),
  classification: v.union([
    v.literal('EXECUTABLE'),
    v.literal('CONFIG'),
    v.literal('DATA'),
    v.literal('BUNDLE')
  ])
})

export const baseSchema = v.object({
  name: v.pipe(v.string(), v.minLength(1)),
  path: v.pipe(v.string(), v.minLength(1)),
  architecture: architectureSchema,
  os: v.string(),
  version: v.string(),
  mode: v.optional(v.union([v.literal('DEBUG'), v.literal('INFO')]), 'INFO')
})

export const configSchema = v.intersect([
  baseSchema,
  v.union([imageSchema, packageSchema])
])
export type Config = v.InferOutput<typeof configSchema>

/**
 * Get configuration options for environment
 */
export const getConfig = () =>
  v.parse(configSchema, {
    name: core.getInput('name'),
    path: core.getInput('path'),
    architecture: core.getInput('architecture'),
    os: core.getInput('os'),
    version: core.getInput('version'),
    type: core.getInput('type'),
    classification: core.getInput('classification'),
    mode: core.getInput('mode')
  })
