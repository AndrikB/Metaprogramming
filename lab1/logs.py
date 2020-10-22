from Formatter import replace_tab_to_space

logs_file = open('errors.log', mode='w+')


def print_log(filename, token_position, message):
    logs_file.write(f'{filename}\t{token_position.row}:{token_position.column}\t:{message}\n')


def write_logs(tokens_before, tokens_after, filename):
    replace_tab_to_space(tokens_before)
    i_before = i_after = 0
    while i_before < len(tokens_before):
        token_before = tokens_before[i_before]
        token_after = tokens_after[i_after]
        if token_before.value == token_after.value:  # all is ok
            i_before += 1
            i_after += 1

        elif token_before.value == ' ':
            print_log(filename, token_before.position, "unexpected space")
            i_before += 1
        elif token_before.value == '\n':
            print_log(filename, token_before.position, "unexpected newline symbol")
            i_before += 1

        elif token_after.value == ' ':
            print_log(filename, token_before.position, "expected space")
            i_after += 1
        elif token_after.value == '\n':
            print_log(filename, token_before.position, "expected newline symbol")
            i_after += 1

        else:
            print(f'wtf\t{token_before}, {token_after}')
