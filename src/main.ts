import * as core from '@actions/core'
import { wait } from './wait'
import { createRunContext } from './context'
import { imageUpload, packageUpload } from './upload';

/**
 * The main function for the action.
 * @returns {Promise<void>} Resolves when the action is complete.
 */
export async function run(): Promise<void> {
  try {
    //const ms: string = core.getInput('milliseconds')

    //// Debug logs are only output if the `ACTIONS_STEP_DEBUG` secret is true
    //core.debug(`Waiting ${ms} milliseconds ...`)

    //// Log the current timestamp, wait, then log the new timestamp
    //core.debug(new Date().toTimeString())
    //await wait(parseInt(ms, 10))
    //core.debug(new Date().toTimeString())

    //// Set outputs for other workflow steps to use
    //core.setOutput('time', new Date().toTimeString())

    // get context
    const ctx = await createRunContext();

    switch (ctx.config.type) {
      case "IMAGE": {
        await imageUpload(ctx);

        break;
      }
      default: {
        await packageUpload(ctx);
      }
    }
  } catch (error) {
    // Fail the workflow run if an error occurs
    if (error instanceof Error) core.setFailed(error.message)
  }
}