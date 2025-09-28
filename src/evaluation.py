import ast

from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ArgumentCorrectnessMetric, TaskCompletionMetric
from deepeval.test_case import LLMTestCase, ToolCall
from langchain_core.messages import AIMessage, ToolMessage
from deepeval.models import GPTModel

MODEL_NAME = "gpt-5-mini"

def retrieval_context_format(result):
    retrieval_context = []
    for message in result["messages"]:
        if isinstance(message, ToolMessage) and message.status == "success":
            retrieval_context.append(message.content)
    return retrieval_context

def tool_calls_format(result):
    tool_calls = []
    tool_calls_tmp = []
    for i in range(len(result["messages"])):
        if isinstance(result["messages"][i], ToolMessage):
            if isinstance(result["messages"][i-1], AIMessage):
                for tool_call in result["messages"][i-1].additional_kwargs["tool_calls"]:
                    tool_calls_tmp.append(
                        tool_call["function"]["arguments"]
                    )
            tool_calls.append(
                ToolCall(
                    name=result["messages"][i].name,
                    output=result["messages"][i].content,
                    input_parameters=ast.literal_eval(tool_calls_tmp[0])
                )
            )
            tool_calls_tmp = tool_calls_tmp[1:]
    return tool_calls


def evaluation(input_message, result, tools):
    evaluation_results = {}
    evaluation_model = GPTModel(
        model=MODEL_NAME,
        temperature=0.0
    )
    test_case = LLMTestCase(
        input=input_message,
        actual_output=result["messages"][-1].content,
        retrieval_context=retrieval_context_format(result),
        tools_called=tool_calls_format(result),
    )

    answer_relevancy = AnswerRelevancyMetric(model=evaluation_model,strict_mode=True)
    faithfulness = FaithfulnessMetric(model=evaluation_model,strict_mode=True)
    argument_correctness = ArgumentCorrectnessMetric(model=evaluation_model,strict_mode=True)
    task_completion = TaskCompletionMetric(model=evaluation_model,strict_mode=True)

    answer_relevancy.measure(test_case)
    evaluation_results['AnswerRelevancyMetric'] = {
        'score': answer_relevancy.score,
        'reason': answer_relevancy.reason,
    }
    faithfulness.measure(test_case)
    evaluation_results['FaithfulnessMetric'] = {
        'score': faithfulness.score,
        'reason': faithfulness.reason,
    }
    argument_correctness.measure(test_case)
    evaluation_results['ArgumentCorrectnessMetric'] = {
        'score': argument_correctness.score,
        'reason': argument_correctness.reason,
    }
    task_completion.measure(test_case)
    evaluation_results['TaskCompletionMetric'] = {
        'score': task_completion.score,
        'reason': task_completion.reason,
    }
    result_str = ""
    for metric, evaluation_result in evaluation_results.items():
        result_str += f"{metric}: {evaluation_result['score']:.2f}/1.00\n"
        result_str += f"Reason: {evaluation_result['reason']}\n"
        result_str += "\n"
    return result_str