def chunk_response_message_into_n_line_chunks(response_message: str, n: int):
    response_message_split_by_new_lines = response_message.split("\n")
    return [
        response_message_split_by_new_lines[i: i + n]
        for i in range(0, len(response_message_split_by_new_lines), n)
    ]
