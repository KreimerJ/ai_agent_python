import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam

from error_catcher import check_api_none, check_usage_response_none
from functions.call_function import available_functions, call_function
from prompts.system_prompt import initial_system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    check_api_none(api_key)
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    args = ai_args_parser()
    messages: list[dict[str, str]] | list[ChatCompletionUserMessageParam] = [
        {"role": "system", "content": initial_system_prompt},
        {
            "role": "user",
            "content": args.user_prompt,
        },
    ]

    broke_before_finishing_loop: bool = False

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions,
        )

        check_usage_response_none(response.usage)

        prompt_token_usage = response.usage.prompt_tokens
        reponse_token_usage = response.usage.completion_tokens
        message = response.choices[0].message
        tool_call_info = message.tool_calls
        messages.append(message)

        if tool_call_info:
            for tool_call in tool_call_info:
                result_message = call_function(tool_call, args.verbose)
                if result_message["content"] == "":
                    raise ValueError(
                        f"Function {tool_call.function.name} returned None"
                    )

                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)

        else:
            output(message.content, prompt_token_usage, reponse_token_usage, args)
            broke_before_finishing_loop = True
            break

    if not broke_before_finishing_loop:
        print(sys.exit(1))


def ai_args_parser():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()

    # Now we can access `args.user_prompt`


def output(message, token_usage, response_usage, args_parser: ai_args_parser):

    if args_parser.verbose:
        print(f"User prompt: {message}")
        print(f"Prompt tokens: {token_usage}")
        print(f"Response tokens: {response_usage}")
    else:
        print(f"Response:{message}")


if __name__ == "__main__":
    main()
