import { backOff } from 'exponential-backoff'
import { TokenData } from './api'
import * as core from '@actions/core'
import { getConfig } from './config'
import { getBackendUrl, getEnv } from './env'
import { BACKOFF_CONFIG } from './constants'

export const createRunContext = async () => {
  const config = getConfig()
  const env = getEnv()
  console.debug(
    `tok len: ${env.CHASSY_TOKEN.length}, ${env.CHASSY_TOKEN.slice(0, 4)}, ${env.CHASSY_TOKEN.slice(env.CHASSY_TOKEN.length - 4, env.CHASSY_TOKEN.length)}`
  )

  // get auth session using refresh token
  const refreshTokenURL = `${getBackendUrl(env).apiBaseUrl}/token/user`
  const tokenRequestBody = {
    token: env.CHASSY_TOKEN
  }
  let refreshTokenResponse: TokenData
  try {
    refreshTokenResponse = await backOff(async () => {
      console.debug(JSON.stringify(tokenRequestBody))
      const rawResponse = await fetch(refreshTokenURL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(tokenRequestBody)
      })
      if (!rawResponse.ok) {
        console.debug(await rawResponse.text())
        throw new Error(`Network response was not ok ${rawResponse.statusText}`)
      }
      return rawResponse.json()
    }, BACKOFF_CONFIG)
  } catch (e) {
    core.error('Failed to refresh token')
    if (e instanceof Error) throw new Error(e.message)
    else throw e
  }

  const authToken = refreshTokenResponse.idToken

  return { config, env, authToken }
}

export type RunContext = Awaited<ReturnType<typeof createRunContext>>
