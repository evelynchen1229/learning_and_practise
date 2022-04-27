def constructor(syntax_file):
    with open(syntax_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        syntaxes = []
        for line in lines:
            syntax = []
            for s in line:
                syntax.append(s)
            syntaxes.append(syntax)

    f.close()

    return syntaxes
