from typing import Optional, List, Dict
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts import (
    WORK_SUMMARY_PROMPT,
    WORK_SUMMARY_SYSTEM_PROMPT,
)
import logging


class WorkSummaryGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(system_prompt=WORK_SUMMARY_SYSTEM_PROMPT)

    def generate_work_summaries(
        self,
        diff_file_data: List[Dict],
        user: Optional[str] = None,
    ):
        available_tokens = self.provider.available_tokens(WORK_SUMMARY_PROMPT)
        summaries = []
        combined_diff_data = ""
        for file_dict in diff_file_data:
            temp_prompt = combined_diff_data
            temp_prompt += f"""\n---->\nFile Name: {file_dict["file"]}\nPatch: {file_dict["patch"]}\n Status: {file_dict["status"]}"""
            if available_tokens - self.provider.get_token_count(temp_prompt) > 0:
                combined_diff_data = temp_prompt
                continue

            # Process the prompt
            prompt = WORK_SUMMARY_PROMPT.format(PATCH_DATA=combined_diff_data)
            response = self.provider.chat_completion(prompt, user=user)
            summaries.append(response)
            combined_diff_data = ""

        if len(summaries) > 1:
            # TODO Merge summaries
            pass

        return summaries[0]